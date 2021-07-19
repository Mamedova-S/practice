import requests
import fake_useragent
from bs4 import BeautifulSoup
import csv

# коодировку
CSV = 'grants2.csv'
URL = 'https://st-gr.com/?cat=3'
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
    items = soup.find('section', class_='content-area').find_all('article', class_='post')
    grants = []

    for  item in items:
        grants.append(
            {
                'title': item.find( 'h1', class_='entry-title').get_text(),
                'deadline': item.find( 'div', class_='entry-summary').find('p').get_text().split('Каждый')[0].split('Дедлайн:')[1],
                'link':  item.find( 'h1', class_='entry-title').find('a').get('href'),

            }
        )
    return grants

def save_csv(items, path):
    with open(path, 'a', newline='') as file:
        writer = csv.writer(file, delimiter= ';')
        # writer.writerow(['Название гранта', 'Дедлайн', 'Ссылка'])
        for item in items:
            writer.writerow([item['title'],item['deadline'],item['link']])


def parser():
    PAGENATION=input('Укажите количество страниц для парсинга:')
    PAGENATION = int(PAGENATION.strip())
    html = get_html(URL)
    if html.status_code == 200:
        grants = []
        for page in range (32,PAGENATION):
            print(f'Парсим страницу: {page})')
            html = get_html(URL, params={'paged': page})
            grants.extend(get_content(html.text))
            save_csv(grants,CSV)
        pass
    else:
        print('Error')

parser()
