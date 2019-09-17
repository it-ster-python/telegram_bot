from bs4 import BeautifulSoup as soup
import requests
import json
import os
import sys
from multiprocessing.dummy import Pool as ThreadPool
import sqlite3
from datetime import datetime


def create_db(path):
    if not os.path.isfile(path):
        with open(path,"wb") as file:
            pass
    return

def get_connect(path):
    connect = sqlite3.connect(path)
    return connect

def create_tables(connect):
    sql_countries = """CREATE TABLE IF NOT EXISTS "countries" (
        "id"    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        "country_name_en" TEXT NOT NULL,
        "country_name_ru" TEXT NOT NULL,
        "country_bin_code" TEXT NOT NULL,
        "image" TEXT NOT NULL
    );
    """
    sql_locations = """CREATE TABLE IF NOT EXISTS "locations" (
        "id"    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        "city_name_en" TEXT NOT NULL,
        "city_name_ru" TEXT NOT NULL,
        "lat" REAL NOT NULL,
        "lon" REAL NOT NULL,
        "country_id" INTEGER NOT NULL,
        FOREIGN KEY (country_id) REFERENCES countries(id)
    );
    """
    cursor = connect.cursor()
    cursor.execute(sql_countries)
    cursor.execute(sql_locations)
    connect.commit()

def get_countries(file_name):
    if os.path.isfile(file_name):
        counties_list = []
        with open(file_name, "r") as html_file:
            html = soup(html_file.read())
            #print(html)
            lines = html.find_all("tr")
            for line in lines:
                rows = line.find_all("td")
                image = rows[0].find("img")
                rus_name = rows[0].text
                bin_code = 





if __name__ == '__main__':

    if len(sys.argv) > 2:
        path = os.path.join(sys.argv[1], sys.argv[2])
        create_db(path)
        connection = get_connect(path)
        create_tables(connection)
        get_countries("countries.html")

