import requests
from bs4 import BeautifulSoup
from urllib import parse


class GoogleCalc():

    def __init__(self, value):
        self.url=self.__create_url(value)

    @staticmethod
    def __create_url(value):
        url=f'https://google.com/search?q={parse.quote(value)}'
        return url

    def get_html(self):
        ua={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36'
        }
        result=requests.get(self.url, headers=ua)
        #VOZMOZHNA OSHIBKA
        self.html=BeautifulSoup(result.text, 'lxml')

    def find_result(self):
        self.result=self.html.find('span', {'id':'cwos'}).text


    def get_result(self):
        return self.result.strip()



if __name__=='__main__':
    calc=GoogleCalc('183 / 4 + cos(30)')
    #print(calc.url)
    calc.get_html()
    #print(calc.html)
    calc.find_result()
    #result=calc.result
    #for element in result:
    #print(element.attrs)
    #print(calc.result)
    print(calc.get_result())
