import json
import sys
import sqlite3
import os
import requests
from bs4 import BeautifulSoup as Bs
from datetime import datetime
from multiprocessing.dummy import Pool as ThreadPool


path = os.path.split(sys.argv[0])[0]
path = os.path.join(path, 'flags/')
path_db = "/home/kirill/telegram_bot/weather/country.db"



def create_db(path_db):
    if not os.path.isfile(path_db):
        with open(path_db, "wb") as file:
            pass
        return


def get_connect(path_db):
    connect = sqlite3.connect(path_db)
    return connect

def create_table(connect):
    sql_countries = """CREATE TABLE IN NOT EXISTS "countries" (
        "id"    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        "image" TEXT NOT NULL,
        "country_name" TEXT NOT NULL,
        "country_code" TEXT NOT NULL
    );
    """
    cursor = connect.cursor()
    cursor.execute(sql_countries)
    connect.commit()

def get_location(path):
    json_file = open(path, "r")
    data = json.load(json_file)
    json_file.close()
    return data

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



def send_data(element, connect):
    sql_countries = f"""INSERT INTO "countries" (
        "image",
        "name",
        "code"
    )
    VALUES (
        {0},
        {1},
        {2},
    );
    """
    cursor = connect.cursor()
    cursor.execute(sql_countries)


if __name__ == '__main__':

    connection = get_connect("city.py")
    data_country = get_country()
    image = os.listdir(path)
    # for image in images:
    #     print(image)
    for id, element in enumerate(data_country, 1):
        len_data = len(data_country)
        print("{0} from {1}".format(id, len_data), end="\r")
        try:
            send_data(country, connection)
        except  Exception as e:
          print("ERROR SQL")
          print(element)
          print(e)
    connection.commit()
