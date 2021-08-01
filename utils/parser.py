import requests
from bs4 import BeautifulSoup


def get_html(url: str) -> str:
    """Получение контента страницы"""
    r = requests.get(url)
    r.encoding = "utf-8"
    if r.status_code == 200:
        return r.text
    else:
        print("Bad status code {}".format(r.status_code))
        return ""


def get_cars(url: str) -> list:
    """Получение списка автомобилий"""
    cars_all = []
    content = get_html(url)
    if not content:
        return cars_all
    soup = BeautifulSoup(content, 'html.parser')
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
