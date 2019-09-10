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
            print(datetime.now())    
            print(flags)
            with open("flags.log", "a") as file:
                file.write("{0}\n{1} >>>> Got sample ({2} images):\n{3}\n".format(sys.argv[0], datetime.now(), len(flags), flags))
            return flags           
        except Exception as e:
            print("Something goes wrong, the following exception was raised:\n{0}".format(e))
            go_further = input("Try to continue one more time? (y/n)")
            if go_further == "n":
                with open("flags.log", "a") as file:
                    file.write("{0} >>> {1}\n".format(datetime.now(), e))
                return
            else:
                with open("flags.log", "a") as file:
                    file.write("{0} >>> The following exception was raised:\n{1}\nTry to continue...\n".format(datetime.now(), e))
                get_html()

    return get_html()


path = os.path.split(sys.argv[0])[0]
path = os.path.join(path, 'flag_images/')
saved_images = []


def create_folder():
    if not os.path.isdir(path):
        try:
            os.mkdir(path)
        except Exception as e:
            with open("flags.log", "a") as file:
                file.write("{0} >>>> Path {1} cannot be created.\nException raised: {2}\n".format(datetime.now(), path, e))

                
def save_image(img): #saves one .gif file

    url_templ = "http://actravel.ru/images/"
    
    if not os.path.isdir(path):
        try:
            os.mkdir(path)
        except Exception as e:
            with open("flags.log", "a") as file:
                file.write("{0} >>>> Path {1} cannot be created, image {2} not saved.\nException raised: {3}".format(datetime.now(), path, img, e))
            #print("Path {0} cannot be created, image {1} not saved. Exception raised:\n{2}".format(path, img, e))
            return
    try:    
        img_file = requests.get(url_templ + img)
        with open(path+img, "wb") as f:
            f.write(img_file.content)
        saved_images.append("{0} >>>> {1} file saved successfully".format(datetime.now(), img))
    except Exception as e:
        saved_images.append("{0} >>>> {1} file not saved!!! Exception raised:\n{2}".format(datetime.now(), img, e))


def demon():
    #pid = os.fork()
    #with open("flags.log", "a") as file:
    #    file.write("Demon started with PID {pid}\n")
    #work = True
    start_script = datetime.now()
    with open("flags.log", "a") as file:
        file.write("{0} >>>> {1} started\n\n".format(datetime.now(), sys.argv))
    create_folder()
    

    def worker():
        try:
            while True: #while work
                sample_len = randint(10, 20)
                #print("I'm going to save {0} random flag images, here are their names:".format(sample_len))
                start = datetime.now()
                pool = ThPool(sample_len)
                results = pool.map(save_image, get_random_flags(sample_len))
                #print("{0} images are saved.".format(len(results)))
                pool.close()
                pool.join()
                finish = datetime.now()
                print(finish - start)
                sleep_time = randint(1, 5)
                print("Now I lay me down to sleep for {0} sec., good night!\n".format(sleep_time))
                with open("flags.log", "a") as file:
                    file.write("{0} >>>> {1} images processed:\n\n".format(datetime.now(), len(saved_images)))
                    for n, im in enumerate(saved_images, 1):
                        with open("flags.log", "a") as file:
                            file.write("{0}\t{1}\n".format(n, im))
                saved_images.clear()
                with open("flags.log", "a") as file:
                    file.write("{0} >>>> Sleeping for {1} sec\n\n".format(datetime.now(), sleep_time))
                time.sleep(sleep_time)                    
                    
        except KeyboardInterrupt:
            try:
                action = input("Should I have a rest? (y/n)")
                if action == "y":
                    with open("flags.log", "a") as file:
                        end_script = datetime.now()
                        file.write("{0} >>>> Interrupted from keyboard\n{1} worked without interruptions.\n\n\n\n\n\n".format(datetime.now(), end_script - start_script))
                    print("Good bye!")
                    return
                else:
                    worker()
                    #pid = os.fork()
            except:
                worker()
                
        except Exception as e:
            with open("flags.log", "a") as file:
                end_script = datetime.now()
                file.write("{0} >>>> Exception raised:\n{1}\n{2} worked without interruptions.\n\n\n\n\n\n".format(datetime.now(), e, end_script - start_script))
            print("Good bye!\nThe following exception raised in worker():\n{0}\n\n\n\n\n\n".format(e))
            return
    worker()


if __name__ == '__main__':
    
    demon()

