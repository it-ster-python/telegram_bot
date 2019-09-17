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

    #proc(saveimg_proc, get_all_country()[:10])

    proc(drive, [30,40,50,60,70,80,90,100])


