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
        "image" TEXT 
    );
    """
    sql_locations = """CREATE TABLE IF NOT EXISTS "locations" (
        "id"    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        "country_code_en" TEXT NOT NULL,
        "city_name_en" TEXT NOT NULL,
        "lat" REAL NOT NULL,
        "lon" REAL NOT NULL,
        "country_id" INTEGER,
        FOREIGN KEY (country_id) REFERENCES countries(id)
    );
    """
    cursor = connect.cursor()
    cursor.execute(sql_countries)
    cursor.execute(sql_locations)
    connect.commit()

def get_countries(file_name):
    if os.path.isfile(file_name):
        countries_list = []
        with open(file_name, "r") as html_file:
            html = soup(html_file.read(), features = "html.parser")
            #print(html)
            lines = html.find_all("tr")
            for line in lines:
                rows = line.find_all("td")
                #image = rows[0].find("img")
                rus_name = rows[0].text
                eng_name = rows[1].text
                bin_code = rows[2].text
                countries_list.append((rus_name, eng_name, bin_code))
    return countries_list

def send_country_data(data, connect):
    sql = f"""INSERT INTO "countries" (
        "country_name_ru",
        "country_name_en",
        "country_bin_code"
        )
        VALUES(
        "{data[0]}",
        "{data[1]}",
        "{data[2]}"
        );
        """
    cursor = connect.cursor()
    cursor.execute(sql)
    connect.commit()

def send_all_countries_data(data_list, connect):
    for data in data_list:
        send_country_data(data, connect)

def get_locations(file_name):
    if os.path.isfile(file_name):
        json_file = open(file_name,"r")
        loc_data = json.load(json_file)
        json_file.close()
        return loc_data
    else:
        return 1

def send_loc_data(data, connect):
    sql = f"""INSERT INTO "locations"(
        "country_code_en",
        "city_name_en",
        "lat",
        "lon"
        )
        VALUES(
        "{data['country']}",
        "{data['name']}",
        "{data['coord']['lat']}",
        "{data['coord']['lon']}"
        );
        """
    cursor = connect.cursor()
    cursor.execute(sql)
    connect.commit()

def send_all_loc_data(data_file, connect):
    for id, data in enumerate (data_file, 1):
        try:
            send_loc_data(data,connect)
        except Exception as e:
            print(e)


if __name__ == '__main__':

    if len(sys.argv) > 2:
        path = os.path.join(sys.argv[1], sys.argv[2])
        create_db(path)
        connection = get_connect(path)
        create_tables(connection)
        countries = get_countries("countries.html")
        #print(countries)
        send_all_countries_data(countries, connection)
        locations = get_locations("city.list.json")
        send_all_loc_data(locations, connection)

