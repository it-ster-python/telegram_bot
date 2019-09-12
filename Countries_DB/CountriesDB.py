import json
import sys
import sqlite3
import os
from bs4 import BeautifulSoup as Bs
import urllib3
import requests


def get_data_ct(file_name):
    if os.path.isfile(file_name):
        result = []
        with open(file_name, "r") as html_file:
            html = Bs(html_file.read())
            lines = html.find_all("tr")
            for line in lines:
                rows = line.find_all("td")
                rus_name = rows[0].text
                bin_code = rows[2].text
                result.append((rus_name,bin_code))
        return result
    else:
        raise ValueError(f"File '{file_name}' not found!")

def create_db(path, file_name):
    path = "/Users/aleksandrtarasenko/Documents/Projects/telegram_bot_itstep/Countries_DB"
    if not os.path.isfile(path):
        output = requests.get(file_name)
        with open(f"file_name", "wb") as file:
            file.write(output.content)


def get_connect(file_name):
    connect = sqlite3.connect(path)
    return connect

def create_table(connect):
    sql_countries = """CREATE TABLE IF NOT EXISTS "countries" (
        "id"    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        "image" TEXT NOT NULL,
        "country_name"    TEXT,
        "country_code"    TEXT NOT NULL,
    );"""
    ql_locations = """CREATE TABLE IF NOT EXISTS "locations" (
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


if __name__ == '__main__':
        res = get_data_ct("countries.html")
        # print(res)
        connection = get_connect("countries.html")

    #     create_table(connection)
    #     data_city_code = get_data("city.list.json")
    #     data_country = get_all_country("countries.html")
    #     len_data = len(data)
    #     for id, element in enumerate(data, 1):
    #         print(f"{id} from {len_data}", end="\r")
    #         try:
    #             send_data(element, connection)
    #         except Exception as e:
    #             print("ERROR SQL")
    #             print(element)
    #             print(e)
    #     connection.commit()
    #     print("\nOK")
    # else:
    #     print("Not arguments")
