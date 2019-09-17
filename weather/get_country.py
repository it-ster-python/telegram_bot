# import bs4.BeautifulSoup as bs
import os
from bs4 import BeautifulSoup as Bs


def get_all_country(file_name):
    if os.path.isfile(file_name):
        result = []
        with open(file_name, "r") as html_file:
            html = Bs(html_file.read())
            lines = html.find_all("tr")
            for line in lines:
                rows = line.find_all("td")
                image = rows[0].find("img")
                rus_name = rows[0].text
                bin_code = rows[2].text
                result.append((image.attrs["src"], rus_name, bin_code))
        return result
    else:
        raise ValueError("File '{0}' not found!".format(file_name))

def get_flags(path):
    pass

def get_sql_country(data):
    pass


if __name__ == '__main__':

    pid = os.getpid()
    print(pid)
    res = get_all_country("countries.html")
    print(res)
