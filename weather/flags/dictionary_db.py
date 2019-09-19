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


def create_table():
        conn = sqlite3.connect("countries_db.db") 
        cursor = conn.cursor()
        try:
            cursor.execute("""CREATE TABLE countries
                  (ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, CODE text, NAME text, FLAG text)
               """)
            write_in_log("Table created successfully")            
        except Exception as e:
            write_in_log("Table not created, exception raised:\n{0}".format(e))


def get_random_word(): #makes sample of .gif file names
    word = input("word:  ")
    
    def get_html():
        ua={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36'
        }
        try:
            url = "https://www.yandex.by/search/?text={0}".format(word)
            result = requests.get(url, headers=ua)
            print(result)
            html = Bs(result, features="html.parser")
            description = html.find_all(attrs={"class":"fact__description typo typo_text_l typo_line_m"})
            print(description)
            #write_in_log("{0}\nGot sample ({1} countries):\n{2}".format(sys.argv[0], len(countries), countries))
            return description
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


if __name__ == '__main__':
    
    get_random_word()


