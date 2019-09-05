from bs4 import BeautifulSoup
def main ():
    my = open ('countries.html')
    soup = BeautifulSoup (my.read(),'html.parser')
    div = soup.find_all ("img", "")
    print (div)
main()

https://habr.com/ru/post/280238/

# http://actravel.ru/images/f_abh.gif


# pip3 install beautifulsoup4
