import os
from bs4 import BeautifulSoup as Bs
import requests
import os
from multiprocessing.dummy import Pool as ThreadPool
from datetime import datetime
import urllib3

url = "http://actravel.ru/country_codes.html"

def get_all_country(file_name):
    if os.path.isfile(file_name):
        result = []
        with open(file_name, "r") as html_file:
            html = Bs(html_file.read())
            lines = html.find_all("tr")
            for line in lines:
                rows = line.find_all("td")
                rus_name = rows[0].text
                bin_code = rows[2].text
                result.append((rus_name, bin_code))
        return result
    else:
        raise ValueError(f"File '{file_name}' not found!")

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
# path = "/home/kirill/telegram_bot/weather/flags/"
def save_image(img):
    url_templ = "http://actravel.ru/images/"
    # print(path+img)
    img_file = requests.get(f"{url_templ} + {img}")
    with open(os.path.join(f"{path} + {img}"), "wb") as file:
        file.write(img_file.content)



if __name__ == '__main__':

    start = datetime.now()
    # pool = ThreadPool(10)
    # results = pool.map(save_images, get_flags())
    # print(len(results))
    # save_images()
    if not os.path.isdir(path):
        os.mkdir(path)
    pool = ThreadPool(10)
    results = pool.map(save_image, get_flags())
    print(len(results))
    pool.close()
    pool.join()
    finish = datetime.now()
    print(finish - start)
    res = get_all_country("countries.html")
    print(res)
