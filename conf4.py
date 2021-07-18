import requests
import fake_useragent
from bs4 import BeautifulSoup as bs
import csv
import re

CSV = 'conf4.csv'
def get_html(url, params= ''):
    user_agent = fake_useragent.UserAgent()
    user = user_agent.random
    headers = {'User-Agent': str(user)}
    r = requests.get(url, headers=headers, params=params)
    return r.text


def get_all_links(html):
    soup = bs(html, 'lxml')
    ads = soup.find('div', class_='panel-col-first').find_all('div', class_='views-row')

    all_links = []

    for index, ad in enumerate(ads):
        link ='https://www.science-community.org' +  ad.find('span', class_='field-content').find('a').get('href')
        all_links.append(link)
        # print(index, link)

    return all_links


def get_page_data(html):
    soup = bs(html, 'lxml')
    info_ = soup.find('div', width='100%').find('div').find_all('p')

    try:
        title = soup.find('section', id='main').find('h1', class_='title').text
    except Exception:
        title = ''
    # print(title)
    try:
        geo = soup.find('section', id='main').find('div', class_='location').find('p').text.split(':')[1]
        geo2 = re.sub("^\s+|\n|\r|\s+$", '', geo)
    except Exception:
        geo2 = ''
    # print(geo2)
    try:
        date = soup.find('section', id='main').find('div', class_='dates').find('span').text
        date2 = re.sub("^\s+|\n|\r|\s+$", '', date)
    except Exception:
        date2 = ''
    # print(date2)
    try:
        deadline = soup.find('section', id='main').find('div', class_='dates').find('p').text.split(':')[1]
        deadline2 = re.sub("^\s+|\n|\r|\s+$", '', deadline)
    except Exception:
        deadline2 = ''
    try:
        field = soup.find('section', id='main').find('div', class_='sciarea').find('p').text.split(':')[1]
        field2 = re.sub("^\s+|\n|\r|\s+$", '', field).split(';')[0]
    except Exception:
        field2 = ''
    try:
        email = soup.find('section', id='main').find('div', class_='confdetails').find_next_sibling('p').text.split(':')[1]
        email2 = re.sub("^\s+|\n|\r|\s+$", '', email)
    except Exception:
        email2 = ''
    try:
        sponsor = soup.find('section', id='main').find('div', class_='confdetails').find_next_sibling('p').find_next_sibling('p').text.text.split(':')[1]
        sponsor2 = re.sub("^\s+|\n|\r|\s+$", '', sponsor)
    except Exception:
        sponsor2 = ''

    try:
        link=info_[11].find('a').get('href')
    except:
        link = 'none'

    print(link)

    data = {
            'title': title,
            'geo2': geo2,
            'date2': date2,
            'deadline': deadline2,
            'field': field2,
            'email': email2,
            'sponsor': sponsor2,
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
                         items['deadline'],
                         items['field'],
                         items['email'],
                         items['sponsor'],
                         items['link']
                         ])

def main():
    # start = datetime.now()
    url ='https://www.science-community.org/ru/conferences'
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
