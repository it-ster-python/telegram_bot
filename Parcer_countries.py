import os
from bs4 import BeautifulSoup as Bs
import urllib3
import requests
from multiprocessing.dummy import Pool as ThPool
from datetime import datetime
import sys


def get_all_country_images(file_name):
    if os.path.isfile(file_name):
        result = []
        with open(file_name, "r") as html_file:
            html = Bs(html_file.read(),features="lxml")
            lines = html.find_all("tr")
            for line in lines:
                rows = line.find_all("td")
                image = rows[0].find("img").attrs["src"][8:]
                result.append(image)
        return result
    else:
        raise ValueError(f"File '{file_name}' not found!")

path = os.path.split(sys.argv[0])[0]
path = os.path.join(path, 'images/')




def save_image(img):
    path = "/Users/aleksandrtarasenko/Documents/Projects/Country_image"
    url = f"http://actravel.ru/images/"
    if not os.path.isdir(path):
        os.mkdir(path)
    output = requests.get(url + img)
    with open(f"{path}/{img}", "wb") as file:
        file.write(output.content)


if __name__ == '__main__':
    start = datetime.now()
    pool = ThPool(10)
    result = pool.map(save_image, get_all_country_images("countries.html"))
    pool.close()
    pool.join()
    stop = datetime.now()
    print(start-stop)
