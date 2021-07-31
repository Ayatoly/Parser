import requests
from bs4 import BeautifulSoup


URL = 'https://auto.ru/moskva/cars/jeep/all/?sort=cr_date-desc&top_days=1'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
    'accept': '*/*'
}


def get_html(url: str, params=None) -> str:
    """Получение контента страницы"""
    r = requests.get(url, headers=HEADERS, params=params)
    if r.status_code == 200:
        return r.content.decode('utf-8')
    else:
        print("Bad status code {}".format(r.status_code))
        return ""

    
def get_content(get_html: str) -> list:
    """Получение списка автомобилий"""
    cars_all = []
    if not get_html:
        return cars_all
    soup = BeautifulSoup(get_html, 'html.parser')
    cars = soup.findAll('div', class_='ListingItem-module__description')
    for car in cars:
        try:
            car_url = car.find('a', class_='Link ListingItemTitle__link').get('href')
            car_price = car.find('div', class_='ListingItemPrice-module__content').text.strip()
            car_region = car.find('span', class_='MetroListPlace__regionName MetroListPlace_nbsp').text.strip()
            carss = [car_url,car_price,car_region]
            cars_all.append(carss)
            print(car_url, car_region, car_price)
        except AttributeError:
            print("Данные не найдены для {}".format(car))
    print(cars_all)
    return cars_all


def parce():
    """Запуск парсера auto.ru"""
    get_content(get_html(url=URL))
