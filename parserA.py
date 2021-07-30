import aiohttp
import scrapy
from bs4 import BeautifulSoup

import requests

url = 'https://auto.ru/moskva/cars/jeep/all/?sort=cr_date-desc&top_days=1'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
    'accept': '*/*'}


class BlogSpider(scrapy.Spider):
    name = "blogspider"
    start_urls = ['https://auto.ru/moskva/cars/jeep/all/?sort=cr_date-desc&top_days=1']

    def parse(self, response, **kwargs):
        for car_div in response.css(".ListingItem-module__listingItem"):
            link = car_div.css("a.ListingItemTitle__link")
            title = link.css("::text").get()
            href = link.css("::attr(href)").get()
            yield {
                'title': title,
                'href': href,
            }


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS,
                     params=params)  # С помощью этого объекта можно получить всю необходимую информацию.
    if r.status_code == 200:
        r = r.content.decode('utf-8')
        return r
    else:
        raise Exception('Cars is empty')


def get_content(get_html):

    soup = BeautifulSoup(get_html, 'html.parser')
    cars = soup.findAll('div', class_='ListingItem-module__description')
    for car in cars:
        try:
            car_url =   car.find('a', class_='Link ListingItemTitle__link').get('href')
            car_price = car.find('div', class_='ListingItemPrice-module__content').text.strip()
            car_region = car.find('span', class_='MetroListPlace__regionName MetroListPlace_nbsp').text.strip()
            print(car_region,car_url,car_price)
            return (car_url,car_price,car_region)
        except Exception:
            raise AttributeError("У этого класса нет такого метода(нет url,нет цены,не указан город)")

get_content(get_html(url=url))
