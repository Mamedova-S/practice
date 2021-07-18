import requests
import fake_useragent
from bs4 import BeautifulSoup
import csv

CSV = 'grants3.csv'
HOST = 'https://st-gr.com'
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
    items = soup.find('main', class_='site-main').find_all('article', class_='type-post')

    for item in items:
        try:
            title = item.find('h1', class_='entry-title').find('a').text.strip()
        # get title
        except:
            title = 'none'
        try:
            link = item.find('h1', class_='entry-title').find('a').get('href')
        # get url
        except:
            link = ' none '
        try:
            deadline = item.find('div', class_='entry-summary').find('p').text.strip()
        # get price
        except:
            deadline = 'none'
        grants = {'title': title, 'link': link, 'deadline': deadline}  # словарь со всеми данными
        save_csv(grants, CSV)



def save_csv(data, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter= ';')
        writer.writerow([data['title'],data['link'],data['deadline']])


def parser():
    html = get_html(URL)
    if html.status_code == 200:
        grants = []
        get_content(html.text)
        pass
    else:
        print('Error')

parser()