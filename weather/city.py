#!/usr/bin/python3
import json
import sys
import sqlite3
import os
from get_country import get_all_country


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



def get_data(path):
    json_file = open(path, "r")
    data = json.load(json_file)
    json_file.close()
    return data

def send_data(element, connect):
    # {'id': 707860, 'name': 'Hurzuf', 'country': 'UA', 'coord': {'lon': 34.283333, 'lat': 44.549999}}
    sql = f"""INSERT INTO "location" (
        "country_code",
        "city",
        "lat",
        "lon"
    )
    VALUES (
        "{element['country']}",
        "{element['name']}",
        {element['coord']['lat']},
        {element['coord']['lon']}
    );
    """
    cursor = connect.cursor()
    cursor.execute(sql)
    # connect.commit()


if __name__ == '__main__':
    if len(sys.argv) > 2:
        path = os.path.join(sys.argv[1], sys.argv[2])
        create_db(path)
        connection = get_connect(path)
        create_table(connection)
        data_city_code = get_data("city.list.json")
        data_country = get_all_country("countries.html")
        len_data = len(data)
        for id, element in enumerate(data, 1):
            print(f"{id} from {len_data}", end="\r")
            try:
                send_data(element, connection)
            except Exception as e:
                print("ERROR SQL")
                print(element)
                print(e)
        connection.commit()
        print("\nOK")
    else:
        print("Not arguments")

# http://actravel.ru/country_codes.html
