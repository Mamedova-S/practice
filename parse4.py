import requests
from bs4 import BeautifulSoup
import csv

def get_html(url):
    r = requests.get(url)
    return r.text

def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')

    pages = soup.find('div', class_='pagination-pages').find_all('a', class_='pagination-page')[-1].get('href')
    # find div, class = pagination-pages, a, class = pagination-pages,take list and last element , href
    # получили '/moskva/telefony?p=60&q=htc'

    total_pages = pages.split('=')[1].split('&')[0]
    # split to "=" and get last page

    return int(total_pages)

def write_csv(data):
    with open('avito.csv', 'a') as f:
        writer  = csv.writer(f)
        writer.writerow( (data['title'],data['price'],data['metro'],data['url']) )

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find('div', class_='catalog-main').find('div', class_='catalog-list').find_all('div', class_='item')
    #get list all ads

    for ad in ads:
        try:
            title = ad.find('div', class_='description').find('h3').text.strip()
        # get title
        except:
            title = 'none'
        try:
            url = 'https://www.avito.ru' + ad.find('div', class_='description').find('a').get('href')
        # get url
        except:
            url = ' none '
        try:
            price = ad.find('div', class_='description').find('div', class_='about').text.strip()
        # get price
        except:
            price = 'none'
        try:
            metro = 'м.' + ad.find('div', class_='description').find('div', class_='data').find('p').text.split()[1]
        # get metro
        except:
            metro = 'none'

        data = {'title': title,'price': price,'metro': metro,'url': url} # словарь со всеми данными

        write_csv(data)

def main():
    url ='https://konferencii.ru/year/2021/30'
    base_url ='https://www.avito.ru/moskva/telefony'
    page_part = 'p='
    query_part = '&q=htc'

    total_pages = get_total_pages(get_html(url))
    # total_pages получает html в результате работы get_html, которому передаем аргумент url

    for i in range(1, total_pages):
        url_gen = base_url + page_part + str(i) + query_part # сгенерировали все урлы
        # print(url_gen)
        html = get_html(url_gen)
        get_page_data(html)

if __name__ == '__main__':
    main()