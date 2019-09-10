import requests
from bs4 import BeautifulSoup


class Job():

    def get_html(self):
        ua = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; \
            rv:67.0) Gecko/20100101 Firefox/67.0'
        }
        response = requests.get('https://hh.ru', headers=ua)
        self.html = response.text

    def get_div(self):
        html = BeautifulSoup(self.html, features="html.parser")
        self.div = html.find_all('div', {'class': 'vacancies-of-the-day__item'})


if __name__ == '__main__':
    a = Job()
    a.get_html()
    a.get_div()
    #print(a.div)
    for every_div in a.div:
        result = every_div.find('span', {'class': 'vacancy-of-the-day__title'})
        print(result.text)
