#!/usr/bin/python3
import json
import sys
import sqlite3
import os
import requests
from bs4 import BeautifulSoup as Bs
from cities_dict import get_cities
from datetime import datetime
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
    

def drive(length, speed):
    hours = length/speed
    days = hours/8
    return days


def executor(index, queue, speed):
    print("Executor start", index)
    days = drive(1500000, speed)
    queue.put("Driving {0} km/h you'll make 15 mln. km in {1} days".format(speed,days))
    print("Executor finish", index)


def proc():
    q = mp.Queue()
    worker = {"nr":"speed"}
    speed = 10
    for i in range(10):
        worker[i] = mp.Process(target=executor, args=(i, q, speed))
        #pid = check_output(["pidof",worker[i]])
        speed+=10

    for i in range(10):
        worker[i].start()
        pid = worker[i].pid
        print(q.get())
        print(pid)
        worker[i].join()


if __name__ == '__main__':

    proc()

    #path = os.path.join(os.path.split(os.path.abspath(__file__))[0],'images_for_db')
    
    #save_all_images(data_country)

    print("\nOK")
        

# http://actravel.ru/country_codes.html
