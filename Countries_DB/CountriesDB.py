import json
import sys
import sqlite3
import os
from datetime import datetime
from bs4 import BeautifulSoup as Bs
import urllib3
import requests
from multiprocessing.dummy import Pool as ThPool

def get_data_ct(file_name):
    if os.path.isfile(file_name):
        result = []
        with open(file_name, "r") as html_file:
            html = Bs(html_file.read(), features="lxml")
            table = html.find_all("table")
            lines = html.find_all("tr")
            for line in lines:
                rows = line.find_all("td")
                image = rows[0].find("img")
                rus_name = rows[0].text
                bin_code = rows[2].text
                result.append((image.attrs["src"],rus_name,bin_code))
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
            write("Done")
    else:
        raise ValueError(f"File '{file_name}' not found!")

def save_image(country):
    img = country[0]
    path = "/Users/aleksandrtarasenko/Documents/Projects/Country_image"
    url = f"http://actravel.ru/images/"
    if not os.path.isdir(path):
        os.mkdir(path)
    output = requests.get(url + img)
    with open(f"{path}/{img}", "wb") as file:
        file.write(output.content)

def save_all_images(countries):
    path = "/Users/aleksandrtarasenko/Documents/Projects/Country_image"
    if not os.path.isdir(path):
        try:
            os.mkdir(path)
        except Exception as e:
            pass

    start = datetime.now()
    pool = ThPool(8)
    result = pool.map(save_image, countries)
    pool.close()
    pool.join()
    stop = datetime.now()
    print(start-stop)

def get_connect(path):
    connect = sqlite3.connect(path)
    return connect

def create_table(connect):
    sql_countries = """CREATE TABLE IF NOT EXISTS "countries" (
        "id"    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        "image" TEXT NOT NULL,
        "country_name"    TEXT,
        "country_code"    TEXT NOT NULL
    );"""
    sql_locations = """CREATE TABLE IF NOT EXISTS "locations" (
        "id"    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        "country_id"    INTEGER NOT NULL,
        "city_ru"    TEXT,
        "city_en"    TEXT NOT NULL,
        "lat"    REAL NOT NULL,
        "lon"    REAL NOT NULL,
        FOREIGN KEY(country_id) REFERENCES countries(id)
    );"""
    cursor = connect.cursor()
    cursor.execute(sql_countries)
    cursor.execute(sql_locations)
    connect.commit()

def get_data_cy(path):
    json_file = open(path, "r")
    data = json.load(json_file)
    json_file.close()
    return data

def add_row_city(city, connection):
    cursor = connection.cursor()
    print(city)
    if city['country'] != "":
        sql = """SELECT id FROM "countries" WHERE country_code='{0}'""".format(city['country'])
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
        except:
            print("ERROR {0} in countries table".format(city['country']))
            return
        cursor.execute(sql)
    else:
        print("ERROR {0}, country_code is empty.".format(city))

def add_row_country(country, connection):
    flag, code, name = country
    cursor = connection.cursor()
    try:
        cursor.execute("""INSERT INTO countries (country_code, country_name, image) VALUES ('{0}', '{1}', '{2}')
                """.format(code, name, flag))
        is_added = True
    except Exception as e:
        ex = e
        is_added = False

    is_added_text = "Row {0} added successfully.".format(country) if is_added else "ERROR {0}, row not added\n Exception raised:\n{1}".format(country, ex)
    print(is_added_text)
    return is_added_text

if __name__ == '__main__':
        connection = get_connect('Weather.db')
        create_table(connection)
        data_country = get_data_ct('countries.html')
        data_city_code = get_data_cy('city.list.json')
for id, element in enumerate(data_country, 1):
    try:
        add_row_country(element, connection)
    except Exception as e:
        print("ERROR SQL")
        print(element)
        print(e)
connection.commit()

for id, element in enumerate(data_city_code[:10], 1):
    try:
        add_row_city(element, connection)
    except Exception as e:
        print("ERROR SQL")
        print(element)
        print(e)
connection.commit()

save_all_images(data_country)

print("Done")
