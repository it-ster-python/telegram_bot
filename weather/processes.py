#!/usr/bin/python3
import json
import sys
import sqlite3
import os
import requests
from bs4 import BeautifulSoup as Bs
from cities_dict import get_cities
from datetime import datetime, date, time, timedelta
from multiprocessing.dummy import Pool as ThPool
import subprocess
import multiprocessing as mp
from subprocess import check_output

def formula_newton(base, exp, startx):
    nextx = (1/exp)*((exp-1)*startx+base/startx**(exp-1))
    return(nextx)


def iterate_newton(base, exp, startx):

    #try:
        #startx = int(base / div)
    #except:
        #startx = base / div
    
    #startx = base / div
        #print(type(startx))
    #print(base, exp, startx)
    result = formula_newton(base, exp, startx)
    delta = 0
    i = 0
    while True:
        #print(base, exp, result)
        result_n = formula_newton(base, exp, result)
        delta_n = (result_n - result)
        #print(i, div, ">>>", result, result_n, delta)
        if abs(delta_n) < 0.000000000000000000000000001:
            return result_n
        else:
            if abs(delta) == abs(delta_n):
                #print(i, div, ">>>", result, result_n, delta)
                return("no result")
            result = result_n
            delta = delta_n
            i+=1

            
def vary_startx(base, exp):
    for i in [1+10**-6, 1+10**-5, 1+10**-4, 1+10**-3, 1+10**-2, 2,3,5,10,50,10**3, 10**3, 10**4, 10**5, 10**10, 10**20, 10**50]:
        try:
            res = iterate_newton(base, exp, i)
            if res == iterate_newton(base, exp, i) != "no result":
                return res
        except:
            pass
        

def find_limit_newton(base, exp):
    try:
        res = vary_startx(base, exp)
        #print(exp, base, " >>> ", res)
        while True:
            base_prev = base
            base = base*10
            #print("exp ", exp, len(str(base)), " >>> ", res)
            res == vary_startx(base, exp)
            if vary_startx(base, exp) != None:
                pass
                #print(vary_startx(base, exp))
            else:
                print("exp {}, base 1e +{} >>> no result".format(exp, len(str(base))))
                res = vary_startx(base_prev, exp)
                print("limit: 1e +", len(str(base))-1)
                print("result: ", res)
                return res
    except:
        #print("base {}, exp {} >>> no result".format(base, exp))
        print(base)
        base = base/10
        while True:
            try:
                res = vary_startx(base, exp)
                print("exp {}, base 1e +{} >>> no result".format(exp, len(str(base*2))))
                l = len(str(base))         
                print("limit: {}".format(l))
                print("result: ", len(str(res)))
                return res
            except:
                #print("base {}, exp {} >>> no result".format(base, exp))
                base = base/2
                
def vary_exp():
    for i in [2,3,4,5,6,7,8,9,10,20,30,40,50,100,500,10**3,10**4, 10**5, 10**6]:
        find_limit_newton(10**50, i)
        


def get_all_country():
    result = []
    html_file = requests.get("http://actravel.ru/country_codes.html").text
    html = Bs(html_file, features="html.parser")
    table = html.find_all("table")[0]
    lines = html.find_all("tr")[1:]
    for line in lines:
        rows = line.find_all("td")
        image = rows[0].find("img")
        rus_name = rows[0].text
        bin_code = rows[2].text
        result.append((image.attrs["src"], rus_name, bin_code))
        country = []
        countries = []
        for line in lines:
            rows = line.find_all("td")
            image = rows[0].find("img").attrs["src"][8:]
            rus_name = rows[0].text
            bin_code = rows[2].text
            country.append(image)
            country.append(bin_code)
            country.append(rus_name)
            countries.append(country)
            country = []
    return countries

def save_image(country): #saves one .gif file
    path = os.path.join(os.path.split(os.path.abspath(__file__))[0],'images_for_db')
    if not os.path.isdir(path):
        try:
            os.mkdir(path)
        except Exception as e:
            pass
    img = country[0]
    url_templ = "http://actravel.ru/images/"
    path = os.path.join(os.path.split(os.path.abspath(__file__))[0],'images_for_db',img)
    try:
        img_file = requests.get(url_templ + img)
        with open(path, "wb") as f:
            f.write(img_file.content)
        is_saved = True
    except Exception as e:
        ex = e
        is_saved = False


def save_all_images(countries):
    path = os.path.join(os.path.split(os.path.abspath(__file__))[0],'images_for_db')
    if not os.path.isdir(path):
        try:
            os.mkdir(path)
        except Exception as e:
            pass

    start = datetime.now()
    pool = ThPool(10)
    results = pool.map(save_image, countries)
    pool.close()
    pool.join()
    finish = datetime.now()
    print(finish - start)
    connection.commit()
    
def plural(nr, word):
    incorrect = {"goos":"gees", "mouse":"mice"}
    if not (word in incorrect.keys()):
        word = word+"s" if nr != 1 else word
    else:
        word = incorrect(word) if nr != 1 else word
    result = "{0} {1}".format(nr, word)
    return(result)
    
    
def drive(index, queue, speed):
    def get_output():
        start = "Get_output start {0}".format(index)
        hours = 15000000/speed
        days = hours/8
        d = date(1,1,1) + timedelta(days)
        days_text = "{0} {1} {2}".format(plural(d.year, "year"),plural(d.month, "month"),plural(d.day, "day"))
        pid_text = ("PID: {0}".format(os.getpid()))
        answer = "Driving {0} km/h you'll make 15 mlns km in {1}".format(speed, days_text)
        finish = "Get_output finish {0}".format(index)
        out = "{0}\n{1}\n{2}\n{3}\n".format(start, pid_text, answer, finish)
        return(out)
    queue.put(get_output())    



def saveimg_proc(index, queue, country):
    def get_output():
        start = "Get_output start {0}".format(index)
        pid_text = ("PID: {0}".format(os.getpid()))
        try:
            save_image(country)
            text = "For {} image saved.".format(country)
        except Exception as e:
            text = "For {0} image not saved!!! exception: {1}".format(country, e)

        finish = "Get_output finish {0}".format(index)
        out = "{}\n{}\n{}\n{}\n".format(start, pid_text, text, finish)
        #print(out)
        return(out)
    queue.put(get_output())


def proc(target, array):
    print("Parent PID: {0}".format(os.getpid()))
    q = mp.Queue()
    worker = {"nr":"proc"}
    i=0
    #countries = get_all_country()[:10]

    for item in array:
        worker[i] = mp.Process(target=target, args=(i, q, item))
        print(worker[i], worker[i].pid, "\n")
        i+=1
    print("\ninitialization complete\n")

    for i in range(len(array)):
        worker[i].start()
        print(worker[i], worker[i].pid, "\n") #dir(worker[i]))
        worker[i].join()         
        print(q.get())
        print(worker[i], worker[i].pid, "\n") #dir(worker[i]))


if __name__ == '__main__':

    #print("result:", find_limit_newton(79999999992,30))
    #print(vary_startx(1298074213335632692498917175172399917694976,3))    

    #proc(saveimg_proc, get_all_country()[:10])

    #proc(drive, [30,40,50,60,70,80,90,100])

    vary_exp()
    
    #print(1000**(1/10000))
    #print(formula_newton(1000, 10000, 2))
    #print(iterate_newton(10**308, 2, 1+10**-6))
    #print(vary_startx(10**309,2))
    
