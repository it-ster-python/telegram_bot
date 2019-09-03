import os
from bs4 import BeautifulSoup as Bs
import urllib
from urllib import parse


def get_all_country_images(file_name):
    if os.path.isfile(file_name):
        result = []
        with open(file_name, "r") as html_file:
            html = Bs(html_file.read(),features="lxml")
            lines = html.find_all("tr")
            for line in lines:
                rows = line.find_all("td")
                image = rows[0].find("img")
                result.append((image.attrs["src"]))
        return result
    else:
        raise ValueError(f"File '{file_name}' not found!")


def __create_url(value):
    url = f"http://actravel.ru?q={parse.quote(value)}"
    return url

def get_image(__create_url):
    resource = urllib.urlopen("url")
    output = open("file01.jpg","wb")
    output.write(resource.read())
    output.close()







if __name__ == '__main__':
    res = get_all_country_images("countries.html")
    print(res)
    value = "/images/f_jp.gif"
    url = __create_url(value)
    print(url)
