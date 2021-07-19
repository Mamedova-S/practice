import requests
import fake_useragent
from bs4 import BeautifulSoup
import csv


CSV = 'grants.csv'
HOST = 'https://guap.ru/science/'
URL = 'https://guap.ru/science/grants'
user_agent = fake_useragent.UserAgent()
user = user_agent.random
HEADERS= {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
     'user-agent': str(user)
}

def get_html(url, params= ''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content (html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='col321')
    grants = []

    for  item in items:
        grants.append(
            {
                'title': item.find( 'div', class_='wt-card-item').find('h4').get_text(),
                'link': HOST + item.find( 'div', class_='wt-card-item').find('a').get('href'),
                'info': item.find( 'div', class_='wt-card-item').find('p').get_text(),
                'date': item.find('div', class_='wt-card-item').find('span').get_text(),

            }
        )
    return grants

def save_csv(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter= ';')
        writer.writerow(['Название гранта', 'Ссылка', 'Описание', 'Дедлайн'])
        for item in items:
            writer.writerow([item['title'],item['link'],item['info'],item['date']])


def parser():
    html = get_html(URL)
    if html.status_code == 200:
        grants = []
        grants.extend(get_content(html.text))
        save_csv(grants, CSV)
        pass
    else:
        print('Error')

parser()