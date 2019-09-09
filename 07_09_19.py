import os
from bs4 import BeautifulSoup as Bs
import requests


def get_all_flag(file_name):
    if os.path.isfile(file_name):
        result = []
        #result = requests.get(file_name).text
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

def save_flags(img):
    if not os.path.isdir(path):
        os.mkdir(path)
    img_file = requests.get(image.attrs["src"])
    with open("image.txt", "wb") as file:
        file.write(img_file.content)


if __name__ =='__main__':
    res = get_all_flag("country.html")
    img_file = open ("image.txt", "w")
    img_file.write(f"\n{res}\n" )
    img_file.close()
