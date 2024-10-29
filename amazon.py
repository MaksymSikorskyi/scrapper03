from requests_html import HTMLSession
from bs4 import BeautifulSoup
import requests


url = 'https://www.amazon.co.uk/s?k=black+friday+deals+2024&crid=2K4LAOZMR1E9J&sprefix=black+friday%2Caps%2C104&ref=nb_sb_ss_ts-doa-p_1_12'

headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

def getdata(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    return soup

def getnextpage(soup):
    page = soup.find('span', {'class': 's-pagination-strip'})
    if not page.find('span', {'class': 's-pagination-item s-pagination-next s-pagination-disabled '}):
        url = 'http://www.amazon.co.uk' + str(page.find)
        return url
    else:
        return

# with open('amazon.html', 'w', encoding='utf-8') as file:
#     file.write(requests.get(url, headers=headers).text)

with open('amazon.html', encoding='utf-8') as file:
    src = file.read()

soup = BeautifulSoup(src, 'lxml')

while True:
    soup = getdata(url)
    url = getnextpage(soup)
    if not url:
        break
    print(url)