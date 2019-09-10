import os
from bs4 import BeautifulSoup as Bs
import requests
from multiprocessing.dummy import Pool as ThPool
from datetime import datetime
import sys
from random import random , sample, randint
import time
import threading as th
import sqlite3

def write_in_log(message):
    with open("countries.log", "a") as file:
        file.write("{0} >>>\t{1}\n".format(datetime.now(), message))


def create_countries_table():
        conn = sqlite3.connect("countries_db.db")
        cursor = conn.cursor()
        try:
            cursor.execute("""CREATE TABLE countries
                  (ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, CODE text, NAME text, FLAG text)
               """)
            write_in_log("Countries table created successfully")
        except Exception as e:
            write_in_log("Countries table not created, exception raised:\n{0}".format(e))


def create_cities_table():
        conn = sqlite3.connect("countries_db.db")
        cursor = conn.cursor()
        try:
            cursor.execute("""CREATE TABLE cities
                  (ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, NAME text, COUNTRY_CODE int FOREIGN KEY REFERENCES countries(ID), LATITUDE real, LONGITUDE real )
               """)
            write_in_log("Cities table created successfully")
        except Exception as e:
            write_in_log("Cities table not created, exception raised:\n{0}".format(e))


def get_countries(): #makes sample of .gif file names

    def get_html():
        try:

            result = requests.get("http://actravel.ru/country_codes.html").text
            html = Bs(result, features="html.parser")
            table = html.find_all("table")[0]
            lines = table.find_all("tr")[1:]
            #results_sample = sample(lines, sample_len)
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
            #print(countries)
            write_in_log("{0}\n({1} countries):\n{2}".format(sys.argv[0], len(countries), countries))
            return countries
        except Exception as e:
            print("Something goes wrong, the following exception was raised:\n{0}\n".format(e))
            go_further = input("Try to continue one more time? (y/n)")
            if go_further == "n":
                write_in_log("The following exception was raised:\n{0}\nClosed by user.".format(e))
                return
            else:
                write_in_log("The following exception was raised:\n{0}\nTry to continue...".format(e))
                get_html()

    return get_html()


path = os.path.split(sys.argv[0])[0]
path = os.path.join(path, 'flag_images/')
countries_counter = 1


def create_folder():
    if not os.path.isdir(path):
        try:
            os.mkdir(path)
        except Exception as e:
            write_in_log("Path {0} cannot be created.\nException raised: {1}".format(path, e))


def save_image(country): #saves one .gif file
    img = country[0]
    url_templ = "http://actravel.ru/images/"

    try:
        img_file = requests.get(url_templ + img)
        with open(path+img, "wb") as f:
            f.write(img_file.content)
        is_saved = True
    except Exception as e:
        ex = e
        is_saved = False

    is_saved_text = "File {0} saved successfully.".format(img) if is_saved else "Something wrong with {0}, file not saved!!!\n Exception raised:\n{1}".format(img, ex)
    return is_saved_text


def add_row_country(country):
    flag, code, name = country
    conn = sqlite3.connect("countries_db.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""INSERT INTO countries (code, name, flag) VALUES ('{0}', '{1}', '{2}')
                """.format(code, name, flag))
        conn.commit()
        is_added = True
    except Exception as e:
        ex = e
        is_added = False

    is_added_text = "Row {0} added successfully.".format(country) if is_added else "Something wrong with {0}, row not added!!!\n Exception raised:\n{1}".format(country, ex)
    return is_added_text


def add_row_city(city):
    conn = sqlite3.connect("countries_db.db")
    cursor = conn.cursor()
    sql = f"""INSERT INTO "cities" (
        "NAME",
        "COUNTRY_CODE",
        "LATITUDE",
        "LONGITUDE"
    )
    VALUES (
        "{city['country']}",
        "{city['name']}",
        {city['coord']['lat']},
        {city['coord']['lon']}
    );
    """
    cursor = connect.cursor()
    cursor.execute(sql)


def get_cities_from_json():

    #path = os.path.join(os.path.split(sys.argv[0])[0],"city.list.json")

    print(os.path.join(os.path.dirname(os.path.abspath(__file__))),"/city.list.json")
    json = open(path, "r")
    cities = json.load(json)
    json.close()
    return cities



def add_row_city(city):
    name, lat, lon, country = city
    conn = sqlite3.connect("countries_db.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""INSERT INTO cities (NAME, COUNTRY_CODE, LATITUDE, LONGITUDE) VALUES ('{0}', '{1}', '{2}')
                """.format(name, country_code, lat, lon))
        conn.commit()
        is_added = True
    except Exception as e:
        ex = e
        is_added = False

    is_added_text = "Row {0} added successfully.".format(country) if is_added else "Something wrong with {0}, row not added!!!\n Exception raised:\n{1}".format(country, ex)
    return is_added_text


def process_country(country):
    global countries_counter
    lock = th.RLock()
    is_saved = save_image(country)
    is_added = add_row_country(country)
    lock.acquire()
    try:
        with open("countries.log", "a") as file:
            file.write("\t{0} >>>> {1}\n".format( datetime.now(), is_saved))
            file.write("\t{0} >>>> {1}\n".format(datetime.now(), is_added))
            countries_counter += 1
    except Exception as e:
        print(e)
    finally:
        lock.release()


def fill_db():
    #pid = os.fork()
    #with open("countries.log", "a") as file:
    #    file.write("Demon started with PID {pid}\n")
    #work = True
    start_script = datetime.now()
    write_in_log("{0} started\n".format(sys.argv))
    create_folder()
    create_cities_table()
    create_countries_table()

    def add_to_db_countries():
        try:
            #while True: #while work
                #global countries_counter
                #sample_len = randint(10, 20)
            countries = get_countries()
            start = datetime.now()
            pool = ThPool(10)
            results = pool.map(process_country, countries)
            pool.close()
            pool.join()
            finish = datetime.now()
            print("countries added  ", finish - start)
                #sleep_time = randint(1, 4)
                #print("Now I lay me down to sleep for {0} sec., good night!".format(sleep_time))
                #write_in_log("{0} countries are processed".format(countries_counter-1))
                #write_in_log("Sleeping for {0} sec\n".format(sleep_time))
                #countries_counter = 1
                #time.sleep(sleep_time)

        except KeyboardInterrupt:
            write_in_log("Interrupted from keyboard")
            try:
                action = input("Should I have a rest? (y/n)")
                if action == "y":
                    end_script = datetime.now()
                    write_in_log("Closed by user\n{0} worked without interruptions.\n\n\n\n\n".format(end_script - start_script))
                    print("Good bye!")
                    return
                else:
                    write_in_log("Try to continue...")
                    add_to_db_countries()
                    #pid = os.fork()
            except:
                add_to_db_countries()

        except Exception as e:
            end_script = datetime.now()
            write_in_log("Exception raised:\n{0}\n{1} worked without interruptions.\n\n\n\n\n".format(e, end_script - start_script))
            print("Good bye!\nThe following exception raised in add_to_db_countries:\n{0}\n\n\n\n\n\n".format(e))
            return

    def add_to_db_cities():
        try:
            cities = get_cities_from_json()[0:20]
            start = datetime.now()
            pool = ThPool(10)
            results = pool.map(add_row_city, cities)
            pool.close()
            pool.join()
            finish = datetime.now()
            print(finish - start)


        except KeyboardInterrupt:
            write_in_log("Interrupted from keyboard")
            try:
                action = input("Should I have a rest? (y/n)")
                if action == "y":
                    end_script = datetime.now()
                    write_in_log("Closed by user\n{0} worked without interruptions.\n\n\n\n\n".format(end_script - start_script))
                    print("Good bye!")
                    return
                else:
                    write_in_log("Try to continue...")
                    add_to_db_cities()
                    #pid = os.fork()
            except:
                add_to_db_cities()

        #except Exception as e:
    #        end_script = datetime.now()
    #        write_in_log("Exception raised:\n{0}\n{1} worked without interruptions.\n\n\n\n\n".format(e, end_script - start_script))
    #        print("Good bye!\nThe following exception raised in add_to_db_cities:\n{0}\n\n\n\n\n\n".format(e))
    #        return

    add_to_db_countries()
    add_to_db_cities()

if __name__ == '__main__':

    fill_db()
