# import bs4.BeautifulSoup as bs
import os
from bs4 import BeautifulSoup as Bs
import requests


def get_all_flag(file_name):
    if os.path.isfile(file_name):
        result = []
        with open(file_name, "r") as html_file:
            html = Bs(html_file.read())
            lines = html.find_all("tr")
            for line in lines:
                rows = line.find_all("td")
                image = rows[0].find("img")
                result.append((image.attrs["src"]))
        return result
    else:
        raise ValueError(f"File '{file_name}' not found!")


def get_save_flag():
    p = requests.get(image.attrs["src"])
    out = out = open("images/f_chk.gif))
    out.write(p.content)
    out.close()






if __name__ == '__main__':
    res = get_all_flag("countries.html")
    print(res)
