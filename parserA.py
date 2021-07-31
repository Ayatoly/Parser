import aiohttp
import scrapy
from bs4 import BeautifulSoup
import requests


URL = 'https://auto.ru/moskva/cars/jeep/all/?sort=cr_date-desc&top_days=1'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
    'accept': '*/*'
}


class BlogSpider(scrapy.Spider):
    name = "blogspider"
    start_urls = ['https://auto.ru/moskva/cars/jeep/all/?sort=cr_date-desc&top_days=1']

    def parse(self, response, **kwargs) -> dict:
        for car_div in response.css(".ListingItem-module__listingItem"):
            link = car_div.css("a.ListingItemTitle__link")
            title = link.css("::text").get()
            href = link.css("::attr(href)").get()
            yield {
                'title': title,
                'href': href,
            }
