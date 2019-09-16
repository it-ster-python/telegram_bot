import os
from bs4 import BeautifulSoup as soup
#from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
import requests
from datetime import datetime

class FlagsImporter():
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
        urls = self.urls
        return urls


    def printUrls(self):
        print(self.urls)

    def downloadFlag(self, url):
        try:
            if not os.path.isdir("flags_imgs"):
                os.mkdir("flags_imgs")
            responce = requests.get(f"{self.main_url}{url}")
            new_file_name = {url.split("/")[-1]}
            #print(new_file_name)
            with open ("{0}/{1}".format("flags_imgs",new_file_name), "wb") as file:
                file.write(responce.content)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    
    importer = FlagsImporter("http://actravel.ru")
    urls = importer.get_urls("countries.html")
    start = datetime.now()
    pool = ThreadPool(6)
    pool.map(importer.downloadFlag, urls)
    pool.close()
    pool.join()
    finish = datetime.now()
    print("Downloding time is   {}".format(finish - start))