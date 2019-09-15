#!/usr/bin/python3
import json
import sys
import sqlite3
import os
from get_country import get_all_country

path = "//home/user/Документы/homework/telegram_bot/country.db"


def create_db(path):
    if not os.path.isfile(path):
        with open(path, "wb") as file:
            pass
    return

def get_connect(path):
    connect = sqlite3.connect(path)
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

def get_data(path):
    json_file = open(path, "r")
    data = json.load(json_file)
    json_file.close()
    return data

def  get_file():
    country = []
    result = requests.get("http://actravel.ru/country_codes.html").text
    html = Bs(result, features="lxml")
    soup = html.find_all("table")[0]
    lines = soup.find_all("tr")[1:]
    for line in lines:
        rows = line.find_all("td")
        image = rows[0].find("img").attrs["src"][8:]
        rus_name = rows[0].text
        bin_code = rows[2].text
        country.append((image.attrs["src"], rus_name, bin_code))
		countries.append(country)
    return countries
    else:
        raise ValueError("File '{0}' not found!".format(file_name))

def send_data(element, connect):
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

    flag, code, name = country
    sql_countries = f"""INSERT INTO "countries" (
        "image",
        "country_name",
        "country_code"
    )
    VALUES (
        {element [image] },
        {element [rus_name]},
        {element[bin_code]}
        );"""


    cursor = connect.cursor()
    cursor.execute(sql_countries)
    cursor.execute(sql_location)
    connect.commit()

if name == 'main':
    #create_db(path)
    connection = get_connect(path)
    #create_table(connection)
    data_city_code = get_data("city.list.json")
    data_country = get_file("http://actravel.ru/country_codes.html")
    len_data = len(data_city_code)
    for id, element in enumerate(data_city_code, 1):
       # print(f"{id} from {len_data}", end="\r")
        try:
            send_data(element, connection)
        except Exception as e:
        #    print("ERROR SQL")
        #   print(element)
        #   print(e)
    connection.commit()
    print("\nOK")




# http://actravel.ru/country_codes.html
