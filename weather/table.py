import json
import sys
import sqlite3
import os
from Parimg import get_all_country

def create_db(path):
    if not os.path.isfile(path):
        with open(path, "wb") as file:
            pass
        return


def get_connect(path):
    connect = sqlite3.connect(path)
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

def get_data(path):
    # json_file = open(path, "r")
    # data = json.load(json_file)
    # json_file.close()
    return data

def send_data(element, connect):
    sql = f"""INSERT INTO "countries" (
        "image",
        "name",
        "code"
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
