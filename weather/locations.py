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


    
def create_db(path):
    if not os.path.isfile(path):
        with open(path, "wb") as file:
            pass
    return


def get_connect(path):
    connect = sqlite3.connect(path)
    return connect


def create_tables(connect):
    sql_countries = """CREATE TABLE IF NOT EXISTS "countries" (
        "id"    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        "image" TEXT NOT NULL,
        "country_name" TEXT NOT NULL,
        "country_code" TEXT NOT NULL UNIQUE
    );
    """
    sql_locations = """CREATE TABLE IF NOT EXISTS "cities" (
        "id"    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        "city"    TEXT NOT NULL,
        "lat"    REAL NOT NULL,
        "lon"    REAL NOT NULL,
        "country_id" INTEGER,
        FOREIGN KEY(country_id) REFERENCES countries(id)
    );"""
    cursor = connect.cursor()
    cursor.execute(sql_countries)
    cursor.execute(sql_locations)
    connect.commit()


def add_row_city(city, connection):
    #connection = get_connect("weather_database.db")
    cursor = connection.cursor()
    # {'id': 707860, 'name': 'Hurzuf', 'country': 'UA', 'coord': {'lon': 34.283333, 'lat': 44.549999}}
    print(city)
    if city['country'] != "":
        sql = """SELECT id FROM "countries" WHERE country_code='{0}'""".format(city['country'])
        print(sql)
        try:
            [country_id], = cursor.execute(sql)
            print(country_id)
            sql = """INSERT INTO "cities" (
                "country_id",
                "city",
                "lat",
                "lon"
            )
            VALUES (
                "{0}",
                "{1}",
                {2},
                {3}
            );
            """.format(country_id, city['name'], city['coord']['lat'], city['coord']['lon'])
            print(sql)
        except:
            print("No {0} in countries table".format(city['country']))
            return
        cursor.execute(sql)
    else:
        print("Row {0} not added, country_code is empty.".format(city))
    # connect.commit()

           
    
def add_row_country(country, connection):
    #connection = get_connect("weather_database.db")
    flag, code, name = country
    cursor = connection.cursor()
    try:
        cursor.execute("""INSERT INTO countries (country_code, country_name, image) VALUES ('{0}', '{1}', '{2}')
                """.format(code, name, flag))
        #connection.commit()
        is_added = True
    except Exception as e:
        ex = e
        is_added = False

    is_added_text = "Row {0} added successfully.".format(country) if is_added else "Something wrong with {0}, row not added!!!\n Exception raised:\n{1}".format(country, ex)
    print(is_added_text)
    return is_added_text


if __name__ == '__main__':
    
    connection = get_connect("weather_database.db")  
    create_tables(connection)
    data_city = get_cities()
    data_country = get_all_country()
    
    #start = datetime.now()
    #pool = ThPool(2)
    #results = pool.map(add_row_country, data_country)
    #pool.close()
    #pool.join()
    #finish = datetime.now()
    #print(finish - start)
    #connection.commit()

    for id, element in enumerate(data_country, 1):
        try:
            add_row_country(element, connection)
        except Exception as e:
            print("ERROR SQL")
            print(element)
            print(e)
    connection.commit()

    for id, element in enumerate(data_city[:100], 1):
        try:
            add_row_city(element, connection)
        except Exception as e:
            print("ERROR SQL")
            print(element)
            print(e)
    connection.commit()

    print("\nOK")
        

# http://actravel.ru/country_codes.html
