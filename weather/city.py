#!/usr/bin/python3
import json
import sys
import sqlite3
import os
import requests
from bs4 import BeautifulSoup as Bs


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
        "country_code" TEXT NOT NULL
    );
    """
    sql_locations = """CREATE TABLE IF NOT EXISTS "cities" (
        "id"    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        "country_code" TEXT,
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

def get_data():
    #json_file = open(path, "r")
    #data = json.load(json_file)
    #json_file.close()
    data = [
  {
    "id": 707860,
    "name": "Hurzuf",
    "country": "UA",
    "coord": {
      "lon": 34.283333,
      "lat": 44.549999
    }
  },
  {
    "id": 519188,
    "name": "Novinki",
    "country": "RU",
    "coord": {
      "lon": 37.666668,
      "lat": 55.683334
    }
  },
  {
    "id": 1283378,
    "name": "Gorkha",
    "country": "NP",
    "coord": {
      "lon": 84.633331,
      "lat": 28
    }
  },
  {
    "id": 1270260,
    "name": "State of Haryana",
    "country": "IN",
    "coord": {
      "lon": 76,
      "lat": 29
    }
  },
  {
    "id": 708546,
    "name": "Holubynka",
    "country": "UA",
    "coord": {
      "lon": 33.900002,
      "lat": 44.599998
    }
  },
  {
    "id": 1283710,
    "name": "Bagmatī Zone",
    "country": "NP",
    "coord": {
      "lon": 85.416664,
      "lat": 28
    }
  },
  {
    "id": 529334,
    "name": "Marina Roshcha",
    "country": "RU",
    "coord": {
      "lon": 37.611111,
      "lat": 55.796391
    }
  },
  {
    "id": 1269750,
    "name": "Republic of India",
    "country": "IN",
    "coord": {
      "lon": 77,
      "lat": 20
    }
  },
  {
    "id": 1283240,
    "name": "Kathmandu",
    "country": "NP",
    "coord": {
      "lon": 85.316666,
      "lat": 27.716667
    }
  },
  {
    "id": 703363,
    "name": "Laspi",
    "country": "UA",
    "coord": {
      "lon": 33.733334,
      "lat": 44.416668
    }
  },
  {
    "id": 3632308,
    "name": "Merida",
    "country": "VE",
    "coord": {
      "lon": -71.144997,
      "lat": 8.598333
    }
  },
  {
    "id": 473537,
    "name": "Vinogradovo",
    "country": "RU",
    "coord": {
      "lon": 38.545555,
      "lat": 55.423332
    }
  },
  {
    "id": 384848,
    "name": "Qarah Gawl al Ulya",
    "country": "IQ",
    "coord": {
      "lon": 45.6325,
      "lat": 35.353889
    }
  },
  {
    "id": 569143,
    "name": "Cherkizovo",
    "country": "RU",
    "coord": {
      "lon": 37.728889,
      "lat": 55.800835
    }
  },
  {
    "id": 713514,
    "name": "Alupka",
    "country": "UA",
    "coord": {
      "lon": 34.049999,
      "lat": 44.416668
    }
  },
  {
    "id": 2878044,
    "name": "Lichtenrade",
    "country": "DE",
    "coord": {
      "lon": 13.40637,
      "lat": 52.398441
    }
  },
  {
    "id": 464176,
    "name": "Zavety Ilicha",
    "country": "RU",
    "coord": {
      "lon": 37.849998,
      "lat": 56.049999
    }
  },
  {
    "id": 295582,
    "name": "Azriqam",
    "country": "IL",
    "coord": {
      "lon": 34.700001,
      "lat": 31.75
    }
  },
  {
    "id": 1271231,
    "name": "Ghura",
    "country": "IN",
    "coord": {
      "lon": 79.883331,
      "lat": 24.766666
    }
  }
]
    
    return data

def add_row_city(city, connect):

    cursor = connect.cursor()
    # {'id': 707860, 'name': 'Hurzuf', 'country': 'UA', 'coord': {'lon': 34.283333, 'lat': 44.549999}}
    sql = """SELECT id FROM "countries" WHERE country_code='{0}'""".format(city['country'])
    print(sql)
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
    cursor.execute(sql)
    # connect.commit()



def get_countries_id(connect):
    cursor = connect.cursor()
    countries_list = {"country": "code"}
    counter = 1
    try:
        while True:
            sql = """SELECT country_code FROM "countries" WHERE id={0}""".format(counter)
            [code], = cursor.execute(sql)
            print(code, counter)
            countries_list[code] = counter
            counter+=1
    except:
        return countries_list
            
    
def add_row_country(country, connect):
    flag, code, name = country
    cursor = connect.cursor()
    try:
        cursor.execute("""INSERT INTO countries (country_code, country_name, image) VALUES ('{0}', '{1}', '{2}')
                """.format(code, name, flag))
        #connect.commit()
        is_added = True
    except Exception as e:
        ex = e
        is_added = False

    is_added_text = "Row {0} added successfully.".format(country) if is_added else "Something wrong with {0}, row not added!!!\n Exception raised:\n{1}".format(country, ex)
    return is_added_text


if __name__ == '__main__':
    if True: #len(sys.argv) > 2:
        #dir_name = os.path.dirname(os.path.abspath(__file__))
        #print(dir_name)
        #path = dir_name+"\city.list.json"
        #print(path)
        #create_db("weather_db")
        connection = get_connect("weather_database.db")
        create_tables(connection)
        data_city = get_data()
        data_country = get_all_country()

        for id, element in enumerate(data_country, 1):
            len_data = len(data_country)
            #print("{0} from {1}".format(id, len_data), end="\r")
            try:
                add_row_country(element, connection)
            except Exception as e:
                print("ERROR SQL")
                print(element)
                print(e)
        connection.commit()
        
        for id, element in enumerate(data_city, 1):
            len_data = len(data_city)
            #print("{0} from {1}".format(id, len_data), end="\r")
            #try:
            add_row_city(element, connection)
            #except Exception as e:
                #print("ERROR SQL")
                #print(element)
                #print(e)
        connection.commit()

        print("\nOK")

    else:
        print("Not arguments")
        

        

# http://actravel.ru/country_codes.html
