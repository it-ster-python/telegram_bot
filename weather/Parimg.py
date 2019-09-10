import os
from bs4 import BeautifulSoup as Bs
import requests
import os
from multiprocessing.dummy import Pool as ThreadPool
from datetime import datetime

url = "http://actravel.ru/country_codes.html"

def get_flags():
    flags = []
    result = requests.get(url).text
    html = Bs(result, features="html.parser")
    table = html.find_all("table")[0]
    lines = table.find_all("tr")[1:]
    for line in lines:
        rows = line.find_all("td")
        image = rows[0].find("img").attrs["src"][8:]
        flags.append(image)
    return flags

path = "/home/kirill/Документы/Projects/telegram_bot/weather/flags/"
def save_images():
    url_templ = "http://actravel.ru/images/"
    if not os.path.isdir(path):
        os.mkdir(path)
    flags = get_flags()
    for flag in flags:
        img_file = requests.get(url_templ + flag)
        with open(os.path.join(path+flag), "wb") as file:
            file.write(img_file.content)



if __name__ == '__main__':

    pool = ThreadPool(len(save_images()))
    start = datetime.now()
    results = pool.map(save_images)
    print(len(results))
    save_images()
    finish = datetime.now()
    pool.close()
    pool.join()
    print(finish - start)
