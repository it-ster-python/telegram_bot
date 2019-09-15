#!/usr/bin/python3
import json
import sys
import sqlite3
import os
import requests
from bs4 import BeautifulSoup as Bs
from datetime import datetime
from multiprocessing.dummy import Pool as ThreadPool



url = "http://actravel.ru/country_codes.html"
path_db = "/home/user/Документы/homework/telegram_bot/weather/city.db"
path = os.path.split(sys.argv[0])[0]
path = os.path.join(path, 'flag_images/')

def get_country():
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

#def save_country(img):
 #   img_file = requests.get(f"http://actravel.ru/{img}")
 #   with open(path+img, "wb") as f:
  #      f.write(img_file.content)
  #  if img_file.status_code == 404:
  #      print("Error")
#    return img_file.content, img

def get_location(path):
    json_file = open(path, "r")
    data = json.load(json_file)
    json_file.close()
    return data

def create_db(path_db):
    if not os.path.isfile(path_db):
        with open(path_db, "wb") as file:
            pass
    return

def get_connect(path_db):
    connect = sqlite3.connect(path_db)
    return connect

def create_table(connect):
    sql_countries = """CREATE TABLE IF NOT EXISTS "countries" (
        "id"    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        "image" TEXT NOT NULL,
        "country_name" TEXT NOT NULL,
        "country_code" TEXT NOT NULL
    );
    """
    sql_locations = """CREATE TABLE IF NOT EXISTS "location" (
        "id"    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        "country_id" INTEGER,
        "city_en"    TEXT NOT NULL,
        "lat"    REAL NOT NULL,
        "lon"    REAL NOT NULL,
        FOREIGN KEY(country_id) REFERENCES countries(id)
    );"""
    cursor = connect.cursor()
    cursor.execute(sql_countries)
    cursor.execute(sql_locations)
    connect.commit()

def send_data_countries(country, connect):
	#country = [image, rus_name, bin_code]
    sql_countries = f"""INSERT INTO "countries" (
        "image",
        "country_name",
        "country_code"
    )
    VALUES (
        {0},
        {1},
        {2}
     )""".format(image, rus_name, bin_code)
    cursor = connect.cursor()
    cursor.execute(sql_countries)
	#connect.commit()

def send_data_location(element, connect):
    sql_location = f"""INSERT INTO "location" (
        "country_id",
        "city_en"
        "lat",
        "lon"
    )
    VALUES (
        (SELECT id FROM countries WHERE "country_code" = "{element}" LIMIT 1),
        "{element['name']}",
        {element['coord']['lat']},
        {element['coord']['lon']}
        );"""

    cursor = connect.cursor()
    cursor.execute(sql_location)
    #connect.commit()

if __name__ == '__main__':
   # start = datetime.now()
    #if not os.path.isdir(path):
      # os.mkdir(path)
    #pool = ThreadPool(10)
  #  res = pool.map( save_country, get_country())
  #  print(len(res))
  #  pool.close()
   # pool.join()
   # finish = datetime.now()
   # print(finish - start)
    #create_db(path_db)
    connection = get_connect("city.py")
    #create_table(connection)
    #data_city_code = get_location("city.list.json")
    #print(data_city_code)
    data_country = get_country()
    #country = [image, rus_name, bin_code]
    image = os.listdir(path)
    for image in images:
        print(image)
    for id, element in enumerate(data_country, 1):
        len_data = len(data_country)
        print("{0} from {1}".format(id, len_data), end="\r")
        try:
            send_data_countries(country, connection)
        except  Exception as e:
          print("ERROR SQL")
          print(element)
          print(e)
    connection.commit()
    data_city_code = get_location("city.list.json")
    len_data = len(data_city_code)
    for id, element in enumerate(data_city_code, 1):
        print(f"{id} from {len_data}", end="\r")
        try:
            send_data_location(element, connection)
            except Exception as e:
                print("ERROR SQL")
                print(element)
                print(e)
    connection.commit()

    