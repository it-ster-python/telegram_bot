import os
from bs4 import BeautifulSoup as Bs
import requests
import sys
import urllib3
from multiprocessing.dummy import Pool as ThreadPool
from datetime import datetime


url = "http://actravel.ru/country_codes.html"
url_pict = "http://actravel.ru/images/"

def get_flags():
    flags = []
    result = requests.get(url).text
    html = Bs(result, features="lxml")
    soup = html.find_all("table")[0]
    lines = soup.find_all("tr")[1:]
    for line in lines:
        rows = line.find_all("td")
        image = rows[0].find("img").attrs["src"][8:]
        flags.append(image)
    return flags

#path = os.path.split(sys.argv[0])[0]
path = os.path.join(path, 'images/')


def save_flags(img):
    if not os.path.isdir(path):
        os.mkdir(path)
    img_file = requests.get(url_pict + img)
    with open(path+img, "wb") as f:
        f.write(img_file.content)
    #return img_file


if __name__ == '__main__':
    #res  = get_flags()
    #print(res)
    start = datetime.now()
    Th_num = len(get_flags())
    pool = ThreadPool(Th_num)
    res = pool.map(save_flags, get_flags())
    print(len(res))
    pool.close()
    pool.join()
    finish = datetime.now()
    print(finish - start)
