import requests, time, json
from bs4 import BeautifulSoup

# with open('data/product_urls', 'r', encoding='utf-8') as file:
#     url = json.load(file)

# print(url)

url = ['https://www.lego.com/uk-ua/product/arctic-explorer-ship-60368', 'https://www.lego.com/uk-ua/product/construction-trucks-and-wrecking-ball-crane-60391', 'https://www.lego.com/uk-ua/product/construction-steamroller-60401']

url1 = 'https://www.lego.com/uk-ua/themes/avatar'
url2 = 'https://www.lego.com/uk-ua/themes/architecture'
url3 = 'https://www.lego.com/uk-ua/themes/creator-3-in-1?page=3&offset=0'



headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }


def get_data(url, headers):
    req = requests.get(url, headers=headers, allow_redirects=False)
    soup = BeautifulSoup(req.text, 'lxml')
    return soup

def cut_url_tail(url):
    return url[:-16]

def get_url_tail(url):
    if url[-3:] == 't=0':
        return url
    else:
        return f'{url}?page=1&offset=0'
    
def no_products_validator(soup):
    no_products = int(soup.find('span', class_='Text__BaseText-sc-13i1y3k-0 kOHdFF').text[-2:])
    if no_products == 0:
        return True
    else:
        return False
    
def one_page_validator(soup):
    one_page = soup.find('div', class_='Paginationstyles__PagesInfo-sc-npbsev-1 gJrFky')
    return one_page

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
    
def get_theme_name(url):
    if url[-3:] == 't=0':
        theme_name = cut_url_tail(url).split('/')[-1]
        return theme_name
    else:
        theme_name = url.split('/')[-1]
        return theme_name
    
def get_product_name(url):
    product_name = '-'.join((url.split('/')[-1]).split('-')[:-1])
    return product_name

def get_product_id(url):
    product_id = (url.split('/')[-1]).split('-')[-1]
    return product_id
    
full_product_data = []

for page in url:
    soup = get_data(page, headers=headers)
    data = soup.find_all('div', class_='ProductGallerystyles__MediaWrapper-sc-1uy048w-1 kBxAec')   
    data2 = soup.find_all('picture', class_='ProductGallerystyles__StyledPicture-sc-1uy048w-4 yhckI')

pictures = []

for page in data2:
    result = page.find('source').get('srcset')
    pictures.append(result)

product_media_urls = []

for i in pictures:
    media_urlset = i.split(', ')
    for x in media_urlset:
        pic = x.split(' ')[0]
        product_media_urls.append(pic)

product_media_full_size_picture = []

for y in product_media_urls:
    if y[-3:] == '1.5':
        product_media_full_size_picture.append(y)

for y in product_media_urls:
    if y[-3:] == '1.5':
        product_media_full_size_picture.append(y)

for y in product_media_urls:
    if y[-3:] == '1.5':
        product_media_full_size_picture.append(y)

name = get_product_name(url[0])

product_id = get_product_id(url[0])

print(product_media_urls)

# разобраться с функциями имени и айди
