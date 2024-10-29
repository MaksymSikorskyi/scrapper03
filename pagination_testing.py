import requests
from bs4 import BeautifulSoup
import time

url = ['https://www.lego.com/uk-ua/themes/creator-3-in-1']
url1 = 'https://www.lego.com/uk-ua/themes/creator-3-in-1'
url2 = 'https://www.lego.com/uk-ua/themes/creator-3-in-1?page=2&offset=0'
url3 = 'https://www.lego.com/uk-ua/themes/creator-3-in-1?page=3&offset=0'



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


while True:
    time.sleep(3)
    soup = get_data(url[-1], headers=headers)
    next_url = get_next_page(soup, url)
    print(next_url)
    if next_url == None:
        print('End of cycle')
        break
    else:
        print('Next')
        url.append(next_url)

    
print(url)

# products = soup.find_all('h3', class_='ProductLeaf_titleRow__KqWbB')

# for product in products:
#     product_url = product.find('a').get('href')
#     lego_crator_product_urls.append(f'https://www.lego.com{product_url}')

# print(lego_crator_product_urls)