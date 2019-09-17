import os
from bs4 import BeautifulSoup as soup
from multiprocessing import Pool
#from multiprocessing.dummy import Pool as ThreadPool
import requests

class FlagsImport():
    def __init__(self, url):
        self.main_url = url
        self.urls = []

    def get_urls(self, file_name):
        try:
            if os.path.isfile(file_name):
                with open(file_name, "r") as html_file:
                    html = soup(html_file.read(), features = "html.parser")
                    images = html.find_all('img')
                    for image in images:
                        self.urls.append(image['src'])
        except Exception as e:
            print(e)

    def printUrls(self):
        print(self.urls)

    def downloadFlags(self):
        try:
            if not os.path.isdir("flags"):
                os.mkdir("flags")
            for url in self.urls:
                responce = requests.get(f"{self.main_url}{url}")
                print(url.split("/")[-1])
                with open(os.path.join("flags", url.split("/")[-1]), "wb") as file:
                    file.write(responce.content)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    importer = FlagsImport("http://actravel.ru")
    importer.get_urls("countries.html")
    importer.downloadFlags()