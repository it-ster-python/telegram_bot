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
                image = rows[0].find("img").src
                rus_name = rows[0].text
                bin_code = rows[2].text
        return result
    else:
        raise ValueError(f"File '{file_name}' not found!")


if __name__ == '__main__':
    main()
