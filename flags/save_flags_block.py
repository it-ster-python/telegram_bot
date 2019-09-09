import os
from bs4 import BeautifulSoup as Bs
import requests
from multiprocessing.dummy import Pool as ThPool
from datetime import datetime
import sys
from random import random , sample, randint
import time
import threading as th

def write_in_log(message):
    with open("flags.log", "a") as file:
        file.write("{0} >>>\t{1}\n".format(datetime.now(), message))
    


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
            write_in_log("{0}\nGot sample ({1} images):\n{2}".format(sys.argv[0], len(flags), flags))
            return flags           
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
images_counter = 1


def create_folder():
    if not os.path.isdir(path):
        try:
            os.mkdir(path)
        except Exception as e:
            write_in_log("Path {0} cannot be created.\nException raised: {1}".format(path, e))
  

def save_image(img): #saves one .gif file
    global images_counter
    lock = th.RLock()
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

    lock.acquire()
    try:
        with open("flags.log", "a") as file:
            file.write("{0}\t{1} >>>> {2}\n".format(images_counter, datetime.now(), is_saved_text))
            images_counter += 1
    except Exception as e:
        print(e)
    finally:
        lock.release()


def demon():
    #pid = os.fork()
    #with open("flags.log", "a") as file:
    #    file.write("Demon started with PID {pid}\n")
    #work = True
    start_script = datetime.now()
    write_in_log("{0} started\n".format(sys.argv))
    create_folder()
    
    
    def worker():
        try:
            while True: #while work
                global images_counter
                sample_len = randint(10, 20)
                #print("I'm going to save {0} random flag images, here are their names:".format(sample_len))
                start = datetime.now()
                pool = ThPool(sample_len)
                results = pool.map(save_image, get_random_flags(sample_len))
                pool.close()
                pool.join()
                finish = datetime.now()
                print(finish - start)
                sleep_time = randint(1, 4)
                print("Now I lay me down to sleep for {0} sec., good night!".format(sleep_time))
                write_in_log("{0} images are processed".format(images_counter-1))                    
                write_in_log("Sleeping for {0} sec\n".format(sleep_time))
                images_counter = 1 
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


