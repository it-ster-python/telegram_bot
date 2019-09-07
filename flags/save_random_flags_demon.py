import os
from bs4 import BeautifulSoup as Bs
import requests
from multiprocessing.dummy import Pool as ThPool
from datetime import datetime
import sys
from random import random , sample, randint
import time


def get_random_flags(sample_len): #makes sample of .gif file names
    
    def get_html():
        try:
            result = requests.get("http://actravel.ru/country_codes.html").text
            html = Bs(result, features="html.parser")
            table = html.find_all("table")[0]
            lines = table.find_all("tr")[1:]
            results_sample = sample(lines, sample_len)
            flags = []
            for line in results_sample:
                rows = line.find_all("td")
                image = rows[0].find("img").attrs["src"][8:]
                flags.append(image)
            print(flags)
            return flags           
        except Exception as e:
            print("Something goes wrong, the following exception was raised:\n{0}".format(e))
            go_further = input("Try to continue one more time? (y/n)")
            if go_further == "n":
                return
            else:
                get_html()

    flags = get_html()
    if flags == None:
        return
    else:
        return flags


path = ""
path_split = sys.argv[0].split('\\')[:-1]
for f in path_split:
    path = path + '\\' + f
path = path[1:]+'\\'+'flag_images'+'\\'
print(path)


def save_image(img): #saves one .gif file

    url_templ = "http://actravel.ru/images/"
    
    if not os.path.isdir(path):
        os.mkdir(path)
    img_file = requests.get(url_templ + img)
    with open(path+img, "wb") as f:
        f.write(img_file.content)


def demon():
    #work = True    
    def worker():
        try:
            while True: #while work
                sample_len = randint(10, 20)
                print("I'm going to save {0} random flag images, here are their names:".format(sample_len))
                start = datetime.now()
                pool = ThPool(sample_len)
                results = pool.map(save_image, get_random_flags(sample_len))
                print("{0} images are saved.".format(len(results)))
                pool.close()
                pool.join()
                finish = datetime.now()
                print(finish - start)
                sleep_time = randint(5, 10)
                print("Now I lay me down to sleep for {0} sec., good night!\n".format(sleep_time))
                time.sleep(sleep_time)
   
        except KeyboardInterrupt:
            try:
                action = input("Should I have a rest? (y/n)")
                if action == "y":
                    print("Good bye!")
                    return
                else:
                    worker()
                    #pid = os.fork()
            except:
                worker()
                
        except Exception as e:
            print("Good bye!\nThe following exception raised in worker():\n{0}".format(e))
            return
    worker()


if __name__ == '__main__':
    
    demon()

