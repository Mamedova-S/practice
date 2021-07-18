import requests
import fake_useragent
from bs4 import BeautifulSoup as bs
import csv
import re


CSV = 'conf2.csv'
# HOST = 'https://expomap.ru'
# URL = 'https://expomap.ru/conference/2021/'
# user_agent = fake_useragent.UserAgent()
# user = user_agent.random
# HEADERS= {
#     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#      'user-agent': str(user)
# }
#
# def get_html(url, params= ''):
#     r = requests.get(url, headers=HEADERS, params=params)
#     return r
#
#
# def get_content (html):
#     soup = BeautifulSoup(html, 'html.parser')
#     items = soup.find_all('li', class_='cl-item')
#     grants = []
#
#     for  item in items:
#         grants.append(
#             {
#                 'title': item.find('div', class_='cli-title').find('a').get_text(),
#                 'link': HOST + item.find( 'div', class_='cli-title').find('a').get('href'),
#                 'info': item.find('div', class_='cli-top').find('div', class_='cli-descr').get_text(strip=True),
#                 'date': item.find('div', class_='cli-date').get_text(strip=True),
#                 'geo': item.find('div', class_='cli-place').get_text(),
#
#
#             }
#         )
#     return grants
#
# def save_csv(items, path):
#     with open(path, 'w') as file:
#         writer = csv.writer(file, delimiter= ';')
#         writer.writerow(['Название гранта', 'Ссылка', 'Описание', 'Дедлайн', 'Место'])
#         for item in items:
#             writer.writerow([item['title'],item['link'],item['info'],item['date'], item['geo']])
# # , encoding ='utf-8'
#
# def parser():
#     PAGENATION = input('Укажите количество страниц для парсинга:')
#     PAGENATION = int(PAGENATION.strip())
#     html = get_html(URL)
#     if html.status_code == 200:
#         grants = []
#         for page in range(1, PAGENATION):
#             print(f'Парсим страницу: {page})')
#             html = get_html(URL, params={'page': page})
#             grants.extend(get_content(html.text))
#             save_csv(grants, CSV)
#         pass
#     else:
#         print('Error')
#
# parser()




def get_html(url, params= ''):
    user_agent = fake_useragent.UserAgent()
    user = user_agent.random
    headers = {'User-Agent': str(user)}
    r = requests.get(url, headers=headers, params=params)
    return r.text


def get_all_links(html):
    soup = bs(html, 'lxml')
    ads = soup.find('div', class_='page-body').find_all('li', class_='cl-item')

    all_links = []

    for index, ad in enumerate(ads):
        link = 'https://expomap.ru/'+ad.find('div', class_='cli-title').find('a').get('href')
        all_links.append(link)
        print(index,link)


    return all_links


def get_page_data(html):
    soup = bs(html, 'lxml')

    try:
        title = soup.find('div', class_='event-page').find('h1', class_='i-title').text
        title2 = re.sub("^\s+|\n|\r|\s+$", '', title)
    except Exception:
        title2 = ''
    # print(title2)
    try:
        geo = soup.find('div', class_='event-page').find('div', class_='address').text
        geo2 = re.sub("^\s+|\n|\r|\s+$", '', geo)
    except Exception:
        geo2 = ''
    # print(geo2)
    try:
        date = soup.find('div', class_='event-page').find('div', class_='i-date').text
        date2 = re.sub("\s*\n\s*", ' ', date)
    except Exception:
        date2 = ''

    try:
        sponsor =soup.find('div', class_='event-page').find('div', class_='event_org').text
        sponsor2 = re.sub("^\s+|\n|\r|\s+$", '', sponsor)
    except Exception:
        sponsor2 = ''

    try:
        link= 'https://expomap.ru'+soup.find('div', class_='event-page').find('li', class_='s1').find('a').get('href').split('/service')[0]
    except:
        link = 'none'

    data = {
            'title2': title2,
            'geo2': geo2,
            'date2': date2,
            'sponsor': sponsor2,
            'link': link,

    }

    save_csv(data, CSV)
    return data


def save_csv(items, path):
    with open(path, 'a',  encoding ='utf-8') as file:
        writer = csv.writer(file, delimiter= ';')
        # writer.writerow(['Название', 'Место', 'Дата проведения', 'Дедлайн', 'Область науки', 'Почта', 'Организатор'])
        writer.writerow([items['title2'],
                         items['geo2'],
                         items['date2'],
                         items['sponsor'],
                         items['link']])

def main():
    # start = datetime.now()
    url ='https://expomap.ru/conference/2021'
    PAGENATION = input('Укажите количество страниц для парсинга:')
    PAGENATION = int(PAGENATION.strip())
    for page in range(1, PAGENATION):
        print(f'Парсим страницу: {page})')
        all_links=get_all_links(get_html(url, params={'page': page}))
        for index, link in enumerate(all_links):
            html = get_html(link)
            get_page_data(html)
        pass
    pass



if __name__ == '__main__':
    main()
