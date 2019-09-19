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
    with open("countries", "a") as file:
        file.write("{0} >>>\t{1}\n".format(datetime.now(), message))


def create_table():
        conn = sqlite3.connect("countries_db.db") 
        cursor = conn.cursor()
        try:
            cursor.execute("""CREATE TABLE countries
                  (country_id real, code text, name text, flag text)
               """)
        except Exception as e:
            write_in_log("Table not created, exception raised:\n{0}".format(e))


def get_random_countries(sample_len): #makes sample of .gif file names
    
    def get_html():
        try:
            result = requests.get("http://actravel.ru/country_codes.html").text
            html = Bs(result, features="html.parser")
            table = html.find_all("table")[0]
            lines = table.find_all("tr")[1:]
            results_sample = sample(lines, sample_len)
            country = []
            countries = []
            for line in results_sample:
                rows = line.find_all("td")
                image = rows[0].find("img").attrs["src"][8:]
                rus_name = rows[0].text
                bin_code = rows[2].text
                country.append(image)
                country.append(bin_code)
                country.append(rus_name)
                countries.append(country)
                country = []
            print(countries)
            write_in_log("{0}\nGot sample ({1} countries):\n{2}".format(sys.argv[0], len(countries), countries))
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


def add_row(country):
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



def process_country(country):
    global countries_counter
    lock = th.RLock()
    is_saved = save_image(country)
    is_added = add_row(country)

    lock.acquire()
    
    try:
        with open("countries", "a") as file:
            file.write("{0}\t{1} >>>> {2}\n".format(countries_counter, datetime.now(), is_saved))
            file.write("\t{0} >>>> {1}\n".format(datetime.now(), is_added))
            countries_counter += 1
    except Exception as e:
        print(e)
    finally:
        lock.release()
                       
                       
def demon():
    #pid = os.fork()
    #with open("countries", "a") as file:
    #    file.write("Demon started with PID {pid}\n")
    #work = True
    start_script = datetime.now()
    write_in_log("{0} started\n".format(sys.argv))
    create_folder()
    create_table()
    
    
    def worker():
        try:
            while True: #while work
                global countries_counter                
                sample_len = randint(10, 20)
                countries = get_random_countries(sample_len)
                start = datetime.now()
                pool = ThPool(sample_len)
                results = pool.map(process_country, countries)
                pool.close()
                pool.join()
                finish = datetime.now()
                print(finish - start)
                sleep_time = randint(1, 4)
                print("Now I lay me down to sleep for {0} sec., good night!".format(sleep_time))
                write_in_log("{0} images are processed".format(countries_counter-1))                    
                write_in_log("Sleeping for {0} sec\n".format(sleep_time))
                countries_counter = 1 
                time.sleep(sleep_time)                    
                    
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
                    worker()
                    #pid = os.fork()
            except:
                worker()
                
        except Exception as e:
            end_script = datetime.now()                    
            write_in_log("Exception raised:\n{0}\n{1} worked without interruptions.\n\n\n\n\n".format(e, end_script - start_script))
            print("Good bye!\nThe following exception raised in worker():\n{0}\n\n\n\n\n\n".format(e))
            return
    worker()


if __name__ == '__main__':
    
    demon()


