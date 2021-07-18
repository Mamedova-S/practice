import requests
import fake_useragent
from bs4 import BeautifulSoup as bs
import selenium
from selenium import webdriver
import time
import mysql.connector
from datetime import datetime


def get_html(url):
    user_agent = fake_useragent.UserAgent()
    user = user_agent.random
    headers = {'User-Agent': str(user)}
    r = requests.get(url, headers=headers)
    return r.text


def get_all_links(html):
    soup = bs(html, 'lxml')
    ads = soup.find('main', class_='site-main').find_all('article', class_='type-post')

    all_links = []

    for index, ad in enumerate(ads):
        link = ad.find('h1', class_='entry-title').find('a').get('href')
        all_links.append(link)

    return all_links


def get_page_data(html):
    soup = bs(html, 'lxml')


    try:
        title = soup.find('article', class_='type-post').find('h1').text
    except Exception:
        title = ''
    try:
        deadline = soup.find('article', class_='type-post').find('p').find('strong').text
    except Exception:
        deadline = ''
    try:
        geolocation = soup.find('article', class_='type-post').find('p').text
    except Exception:
        geolocation = ''

    print(deadline)
    # try:
    #     phone = soup.find('div', class_='_1DzgK').find('a').get('href')[5::1]
    # except Exception:
    #     phone = ''
    # try:
    #     url = 'https://m.avito.ru' + soup.find('div', class_='_1PRsv').find('a').get(
    #         'href').split('/abuse')[0]
    # except Exception:
    #     url = ''
    #
    # data = {'id': id2,
    #         'title': title,
    #         'price': price,
    #         'address': address,
    #         'phone': phone,
    #         'url': url}
    #
    # write_sql(data)
    # return data


# def scroll(url):
#     user_agent = fake_useragent.UserAgent()
#     user = user_agent.random
#
#     options = selenium.webdriver.ChromeOptions()
#     options.add_argument('--headless')
#     options.add_argument(str(user))
#
#     browser = webdriver.Chrome(options=options)
#     browser.get(url)
#
#     SCROLL_PAUSE_TIME = 1
#
#     last_height = browser.execute_script("return document.body.scrollHeight")
#
#     while True:
#         browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         new_height = browser.execute_script("return document.body.scrollHeight")
#
#         time.sleep(SCROLL_PAUSE_TIME)
#
#         if new_height == last_height:
#             break
#         last_height = new_height
#
#     return browser.page_source
#
#
# def write_sql(data):
#     dbconfig = {'host': '127.0.0.1',
#                 'user': 'testuser1234',
#                 'password': 'password1234',
#                 'database': 'avitodb'}
#
#     conn = mysql.connector.connect(**dbconfig)
#     cursor = conn.cursor()
#
#     _SQL = """replace into avitodb.`table` (id, title, price, address, phone, url) values (%s,%s,
#     %s,%s,%s,%s)"""
#
#     cursor.execute(_SQL, (data['id'],
#                           data['title'],
#                           data['price'],
#                           data['address'],
#                           data['phone'],
#                           data['url']))
#
#     conn.commit()
#     cursor.close()
#     conn.close()
#

def main():
    # start = datetime.now()
    url = 'https://st-gr.com/?cat=3'
    all_links = get_all_links(get_html(url))

    for index, link in enumerate(all_links):
        html = get_html(link)
        data = get_page_data(html)

    # end = datetime.now()
    # total = end - start
    # print(total)


if __name__ == '__main__':
    main()

















# import selenium
# from selenium import webdriver
# import time
# import mysql.connector
# from datetime import datetime
#
# CSV = 'grants2.csv'
#
# def get_html(url):
#     r = requests.get(url)
#     return r.text
#
# def get_all_links(html):
#     soup = BeautifulSoup(html, 'lxml')
#     tds = soup.find('div', class_='post-list').find_all('h2', class_='post-title')
#     links = []
#     for td in tds:
#         a = td.find('a').get('href')
#         link = 'https://vsekonkursy.ru' + a
#         links.append(link)
#
#     return links
#
#
# def get_page_data(html):
#     soup = BeautifulSoup(html, 'lxml')
#     try:
#         name = soup.find('h1', class_='post-title').text.strip()
#     except:
#         name= ''
#
#     try:
#         organization = soup.find('div', class_='entry-inner').text.strip()
#     except:
#         organization= ''
#
#     try:
#         prize = soup.find('div', class_='entry-inner').find('ul').text.strip()
#     except:
#         prize = ''
#
#         data = { 'name': name,
#         'organization': organization,
#         'prize': prize }
#
# def write_csv(data,path ):
#     with open(path, 'w', newline='') as file:
#         writer = csv.writer(file, delimiter= ';')
#         writer.writerow(['Название гранта', 'Организатор', 'Приз'])
#
#         writer.writerow((data['name'],
#                          data['organization'],
#                          data['prize'],
#                          ))
#
#
#
#
#
# def main():
#     url = 'https://vsekonkursy.ru/granty-2019'
#     all_links = get_all_links(get_html(url))
#
#     for i in all_links:
#         html =get_html(url)
#         data = get_page_data(html)
#         write_csv(data)
#
#
