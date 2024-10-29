import requests
from bs4 import BeautifulSoup
import time


url = 'https://www.lego.com/uk-ua/themes'
lego_paginated_urls = []
lego_theme_url_list = []
theme_name_list = []
theme_url = []
products_url = []


headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }


def get_data(url, headers):
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, 'lxml')
    return soup

def cut_url_tail(url):
    return url[:-16]

def get_url_tail(url):
    if url[-3:] == 't=0':
        return url
    else:
        return f'{url}?page=1&offset=0'
    
def get_theme_name(url):
    if url[-3:] == 't=0':
        theme_name = cut_url_tail(url).split('/')[-1]
        return theme_name
    else:
        theme_name = url.split('/')[-1]
        return theme_name

def one_page_validator(soup):
    one_page = soup.find('div', class_='Paginationstyles__PagesInfo-sc-npbsev-1 gJrFky')
    return one_page

def no_products_validator(soup):
    no_products = int(soup.find('span', class_='Text__BaseText-sc-13i1y3k-0 kOHdFF').text[-2:])
    if no_products == 0:
        return True
    else:
        return False

def get_next_page(soup, url):
    page = soup.find('span', class_='Paginationstyles__NextLinkDisabled-sc-npbsev-12 kShVNO')
    if page is None:
        if url[-1][-3:] == 't=0':
            next_url = f'{cut_url_tail(url[-1])}?page={int(len(url) + 1)}&offset=0'
            return next_url
        else:
            next_url = f'{url[-1]}?page={int(len(url) + 1)}&offset=0'
            return next_url          
    else:
        return None

def get_product_name(url):
    product_name = '-'.join((url.split('/')[-1]).split('-')[:-1])
    return product_name

def get_product_id(url):
    product_id = (url.split('/')[-1]).split('-')[-1]
    return product_id

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

soup = get_data(url, headers=headers)

articles = soup.find_all("article", class_='CategoryLeafstyles__Wrapper-sc-is33yg-0 leEFcr')

for article in articles:
    lego_theme_url = article.find('a').get('href')
    lego_theme_url_list.append(f'https://www.lego.com{lego_theme_url}')

# print(len(lego_theme_url_list))
# time.sleep(10)

for url in lego_theme_url_list:
    print('next theme url')
    # time.sleep(1)
    theme_url.append(url)

    while True:
        time.sleep(1)
        soup = get_data(theme_url[-1], headers=headers)
        next_url = get_next_page(soup, theme_url)
        one_url = one_page_validator(soup)

        if no_products_validator(soup) == True:
            break

        if one_url is not None:
            print('one url')
            lego_paginated_urls.append(theme_url[-1])
            theme_url.clear()
            print(theme_url)
            # time.sleep(2)
            break

        if next_url == None:
            print('last url')
            lego_paginated_urls.append(theme_url[0])
            theme_url.clear()
            print(theme_url)
            # time.sleep(2)
            break
        else:
            print('paginated url collect')
            theme_url.append(next_url)
            print(theme_url)
            lego_paginated_urls.append(theme_url[-1])
            # time.sleep(2)

    theme_url.clear()

    print('While done')
    print(lego_paginated_urls)
    # time.sleep(2)

# for url in lego_paginated_urls:
#     with open('lego_paginated_urls.txt', 'w+', encoding='utf-8') as file:
        # file.write(url)
for url in lego_paginated_urls:
    # time.sleep(1)
    soup = get_data(url, headers=headers)
    products = soup.find_all('h3', class_='ProductLeaf_titleRow__KqWbB')

    for product in products:
        product_url = product.find('a').get('href')
        products_url.append(f'https://www.lego.com{product_url}')
    
    # lego_paginated_urls.clear

print(products_url)
