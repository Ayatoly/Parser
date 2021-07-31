import requests
from bs4 import BeautifulSoup


def get_html(url: str, params=None) -> str:
    """Получение контента страницы"""
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
        'accept': '*/*'
    }
    r = requests.get(url, headers=headers, params=params)
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
