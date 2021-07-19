import requests
import fake_useragent
from bs4 import BeautifulSoup as bs
import csv
import re

# не получается спарсить все страницы
CSV = 'conf1.csv'
def get_html(url, params= ''):
    user_agent = fake_useragent.UserAgent()
    user = user_agent.random
    headers = {'User-Agent': str(user)}
    r = requests.get(url, headers=headers, params=params)
    return r.text

def get_all_links(html):
    soup = bs(html, 'lxml')
    ads = soup.find('div', class_='content').find_all('div', class_='index_cat_txt')

    all_links = []

    for index, ad in enumerate(ads):
        link = 'https://konferencii.ru' + ad.find('div', class_='index_cat_tit').find('a').get('href')
        all_links.append(link)


    return all_links


def get_page_data(html):
    soup = bs(html, 'html.parser')
    info_ = soup.find('div', class_='content').find('div', class_='left-col').find_all('p')
    # items = soup.find('div', id='right_col').find_all('div', class_='index_cat_1st')

    try:
        title = soup.find('div', class_='content').find('h1', class_='inside_h1a').text
        # get title
    except:
        title = 'none'
    try:
        geo = soup.find('div', class_='content').find('p', class_='city').text.split('(')[0]
        geo2= re.sub("^\s+|\n|\r|\s+$", '', geo)
        # get title
    except:
        geo2 = 'none'
    try:
        form = info_[1].text.split('Форма участия: ')[1]
        form2= re.sub("^\s+|\n|\r|\s+$", '', form)
    except:
        form2 = 'none'
    try:
        date = soup.find('div', class_='content').find('div', id='main_top').find('p').text.split(', срок заявок:')[0]
        date2=re.sub("^\s+|\n|\r|\s+$", '', date)
    except:
        date2 = 'none'
    try:
        deadline = soup.find('div', class_='content').find('div', id='main_top').find('p').text
        deadline2=re.sub("^\s+|\n|\r|\s+$", '', deadline.split('срок заявок:')[1])
    except:
        deadline2 = 'none'
    try:
        organizator=info_[5].text.split('Организаторы: ')[1]
    except:
        organizator = 'none'
    try:
        email=info_[7].text.split('Эл. почта: ')[1]
    except:
        email = 'none'
    try:
        link='https://konferencii.ru' + soup.find('div', class_='content').find('div', class_='lang').find('a').get('href')
    except:
        link = 'none'

    data = {'title': title, 'geo2': geo2, 'form2': form2, 'date2': date2, 'deadline2': deadline2,  'organizator': organizator,  'email': email,  'link': link}  # словарь со всеми данными
    save_csv(data, CSV)
    return data


def save_csv(items, path):
    with open(path, 'a', newline='') as file:
        writer = csv.writer(file, delimiter= ';')
        # writer.writerow(['Название', 'Место', 'Форма участия', 'Дата', 'Дедлайн', 'Организатор', 'Почта', 'Ссылка'])
        writer.writerow((items['title'],
                         items['geo2'],
                         items['form2'],
                         items['date2'],
                         items['deadline2'],
                         items['organizator'],
                         items['email'],
                         items['link'] ))



def main():

    # 29 страниц

    url = 'https://konferencii.ru/year/2021/29'
    all_links = get_all_links(get_html(url))

    for index, link in enumerate(all_links):
        html = get_html(link)
        data = get_page_data(html)

if __name__ == '__main__':
    main()
