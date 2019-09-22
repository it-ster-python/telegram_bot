import json
import sys
import sqlite3
import os
import requests
from bs4 import BeautifulSoup as Bs
from datetime import datetime
from multiprocessing.dummy import Pool as ThreadPool
from get_country import get_all_country

path = os.path.split(sys.argv[0])[0]
path = os.path.join(path, 'flags/')
path_db = "/home/kirill/telegram_bot/weather/country.db"

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
            country.append(rus_name)
            country.append(bin_code)
            countries.append(country)
            country = []
    return countries

def create_db(path_db):
    if not os.path.isfile(path_db):
        with open(path.db, "wb") as file:
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
        "city_en"    TEXT NOT NULL,
        "country_code" TEXT NOT NULL,
        "lat"    REAL NOT NULL,
        "lon"    REAL NOT NULL,
        FOREIGN KEY(country_id) REFERENCES countries(id)
    );"""
    cursor = connect.cursor()
    cursor.execute(sql_countries)
    cursor.execute(sql_locations)
    connect.commit()


def get_location(path):
    json_file = open(path, "r")
    data = json.load(json_file)
    json_file.close()
    return data


def send_data(element, connect):
    sql_countries = f"""INSERT INTO "countries" (
        "image",
        "country_name",
        "country_code"
    )
    VALUES (
        "{element[0]}",
        "{element[1]}",
        "{element[2]}"
    );
    """
    # print(sql_countries)
    # raise ValueError()

    sql_location = f"""INSERT INTO "location" (
        "country_code",
        "city_en",
        "lat",
        "lon"
    )
    VALUES (
        (SELECT id FROM countries WHERE "country_code" = "{element}" LIMIT 1),
        "{element['name']}",
        {element['coord']['lat']},
        {element['coord']['lon']}
    );
    """

    cursor = connect.cursor()
    cursor.execute(sql_countries)
    cursor.execute(sql_location)
    connect.commit()



if __name__ == '__main__':

    connection = get_connect("country.db")
    # data_country = get_country()
    data_city_code = get_location("city.list.json")
    data_country = get_country()
    image = os.listdir(path)
        # for image in images:
    #     print(image)
    len_data = len(data_country)
    for id, element in enumerate(data_country, 1):
        print("{0} from {1}".format(id, len_data), end="\r")
        # print(element)
        try:
            send_data(element, connection)
        except Exception as e:
            print("ERROR SQL")
            print(element)
            print(e)
