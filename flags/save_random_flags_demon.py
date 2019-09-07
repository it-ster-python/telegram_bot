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

#if "\\" in sys.argv[0]:
#    path_split = sys.argv[0].split('\\')[:-1]
#else:
#    path_split = sys.argv[0].split('/')[:-1]
#for f in path_split:
#    path = path + '/' + f
#path = path[1:]+'/'+'flag_images'+'/'

path = os.path.split(sys.argv[0])[0]
path = os.path.join(path, 'flag_images/')

def save_image(img): #saves one .gif file

    url_templ = "http://actravel.ru/images/"
    
    if not os.path.isdir(path):
        try:
            os.mkdir(path)
        except Exception as e:
            print("Path {0} cannot be created, image {1} not saved. Exception raised:\n{2}".format(path, img, e))
            return
    try:    
        img_file = requests.get(url_templ + img)
        with open(path+img, "wb") as f:
            f.write(img_file.content)
    except Exception as e:
        print("Something wrong with image {0}, file not saved. Exception raised:\n{1}".format(img, e))
        return


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


