
import requests
from bs4 import BeautifulSoup
import csv
import sqlite3

URL = 'https://auto.ria.com/newauto/marka-jeep/'
HEADERS = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
           'accept':'*/*'}
host = 'https://auto.ria.com'
FILE = 'cars.csv'
links1 = []
def get_html(url, params=None):
    r = requests.get(url,headers=HEADERS, params=params) #С помощью этого объекта можно получить всю необходимую информацию.
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.findAll('div', class_='proposition')

    cars = []
    connection = sqlite3.connect('db.db')
    cursor = connection.cursor()
    for item in items:
        cars.append({
            'title': item.find('h3', class_="proposition_name").get_text(strip=True),
            'link': host+item.find('a', class_="proposition_link").get('href'),
            'city': item.find('span', class_='item region').text.strip(),
            'price': item.find('div', class_='proposition_price').text.strip()[:9]
        })
        with connection:
            cursor.execute('INSERT INTO "link" (url) VALUES (?)',[item.find('a', class_="proposition_link").get('href')])
    connection.commit()
    connection.close()
        #if  item.find('a', class_="proposition_link").get('href') not in links1:

        #    links1.append(item.find('a', class_="proposition_link").get('href'))
    for i in cars:

        print(i['title'],i['link'],i['price'][:9],i['city'])

    print(len(cars))
    return cars

def save_file(items,path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file) #, dialect=';')
        writer.writerow(['Марка','ссылка','цена','город'])
        for item in items:
            writer.writerow([item['title'],item['link'],item['city'],item['price']])


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        cars = get_content(html.text)
        save_file(cars,FILE)
        print(len(links1))
    else:
        print('Error')


parse()


connection = sqlite3.connect('db.db')
cursor = connection.cursor()
