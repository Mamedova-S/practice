import requests
import fake_useragent
from bs4 import BeautifulSoup as bs
import csv
import re

CSV = 'conf5.csv'
def get_html(url, params= ''):
    user_agent = fake_useragent.UserAgent()
    user = user_agent.random
    headers = {'User-Agent': str(user)}
    r = requests.get(url, headers=headers, params=params)
    return r.text


def get_all_links(html):
    soup = bs(html, 'lxml')
    ads = soup.find('div', class_='list-view').find_all('div', class_='row-fluid event-head')

    all_links = []

    for index, ad in enumerate(ads):
        link ='https://konferen.ru' +  ad.find('div', class_='span10').find('a').get('href')
        all_links.append(link)


    return all_links


def get_page_data(html):
    soup = bs(html, 'lxml')
    info_ = soup.find('section', class_='span9 content').find('div', class_='span8').find_all('i')

    try:
        title = soup.find('section', class_='span9 content').find('div', class_='span8').find('h4').text
    except Exception:
        title = ''
    try:
        geo = soup.find('section', class_='span9 content').find('div', class_='row-fluid event-pre').find('p').text.split('Email')[0]
        geo2 = re.sub("^\s+|\n|\r|\s+$", '', geo.split('Место')[1])
    except Exception:
        geo2 = ''
    try:
        date = soup.find('section', class_='span9 content').find('div', class_='span8').find('i').text
        date2 = re.sub("\s*\n\s*", '', date)
    except Exception:
        date2 = ''
    try:
        deadline = info_[1].text
        deadline2 = re.sub("^\s+|\n|\r|\s+$", '', deadline)
    except Exception:
        deadline2 = ''
    try:
        email = soup.find('section', class_='span9 content').find('div', class_='row-fluid event-pre').find('p').text.split('Email')[1]
        email2 = re.sub("^\s+|\n|\r|\s+$", '', email)
    except Exception:
        email2 = ''
    try:
        sponsor = soup.find('section', class_='span9 content').find('div', class_='row-fluid event-pre').\
            find('table').find('i').text
    except Exception:
        sponsor = ''
    try:
        link='https://konferen.ru/preview/' + soup.find('section', class_='span9 content').\
            find('a', class_='btn tender').get('href').split('tender/')[1]
    except:
        link = 'none'


    data = {
            'title': title,
            'geo2': geo2,
            'date2': date2,
            'deadline2': deadline2,
            'email2': email2,
            'sponsor': sponsor,
            'link': link,
    }

    save_csv(data, CSV)
    return data


def save_csv(items, path):
    with open(path, 'a',encoding ='utf-8') as file:
        writer = csv.writer(file, delimiter= ';')
        # writer.writerow(['Название', 'Место', 'Дата проведения', 'Дедлайн', 'Область науки', 'Почта', 'Организатор'])
        writer.writerow([items['title'],
                         items['geo2'],
                         items['date2'],
                         items['deadline2'],
                         items['email2'],
                         items['sponsor'],
                         items['link']
                         ])

def main():
    # start = datetime.now()
    url ='https://konferen.ru/?Event%5Btitle%5D=&Event%5Brf_country%5D=&Event%5Brf_city%5D=&Event%5Bdate_b%5D=18.07.2021&Event%5Bdate_e%5D=&Event%5Bis_getin%5D=1&yt1='
    PAGENATION = input('Укажите количество страниц для парсинга:')
    PAGENATION = int(PAGENATION.strip())
    for page in range(1, PAGENATION):
        print(f'Парсим страницу: {page})')
        all_links=get_all_links(get_html(url, params={'events': page}))
        for index, link in enumerate(all_links):
            html = get_html(link)
            get_page_data(html)
        pass
    pass



if __name__ == '__main__':
    main()
