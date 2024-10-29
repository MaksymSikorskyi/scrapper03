import requests, time, json, datetime
from bs4 import BeautifulSoup


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
    product_name = ' '.join((url.split('/')[-1]).split('-')[:-1])
    return product_name

def get_product_id(url):
    product_id = (url.split('/')[-1]).split('-')[-1]
    return product_id

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
print(datetime.datetime.now())
soup = get_data(url, headers=headers)

articles = soup.find_all("article", class_='CategoryLeafstyles__Wrapper-sc-is33yg-0 leEFcr')

for article in articles:
    lego_theme_url = article.find('a').get('href')
    lego_theme_url_list.append(f'https://www.lego.com{lego_theme_url}')

for url in lego_theme_url_list:
    # print('next theme url')
    # time.sleep(1)
    theme_url.append(url)

    while True:
        # time.sleep(1)
        soup = get_data(theme_url[-1], headers=headers)
        next_url = get_next_page(soup, theme_url)
        one_url = one_page_validator(soup)

        if no_products_validator(soup) == True:
            break

        if one_url is not None:
            # print('one url')
            lego_paginated_urls.append(theme_url[-1])
            theme_url.clear()
            # print(theme_url)
            # time.sleep(2)
            break

        if next_url == None:
            # print('last url')
            lego_paginated_urls.append(theme_url[0])
            theme_url.clear()
            # print(theme_url)
            # time.sleep(2)
            break
        else:
            # print('paginated url collect')
            theme_url.append(next_url)
            lego_paginated_urls.append(theme_url[-1])
            # time.sleep(2)

    theme_url.clear()

print('Paginated urls collecting complete.')
print(datetime.datetime.now())

for url in lego_paginated_urls:
    # time.sleep(1)
    soup = get_data(url, headers=headers)
    products = soup.find_all('h3', class_='ProductLeaf_titleRow__KqWbB')

    for product in products:
        product_url = product.find('a').get('href')
        products_url.append(f'https://www.lego.com{product_url}')
    
    # lego_paginated_urls.clear

with open('data/product_urls', 'a', encoding='utf-8') as file:
    json.dump(products_url, file, indent=4, ensure_ascii=False)

print('Collecting product urls complete')
print(datetime.datetime.now())

# full_products_data = []
# raw_mediaset = []
# product_media_urls = []
# product_media_full_size_picture = []

# page_count = 0
# print(products_url)
# for page in products_url:
#     product_data = {
#         'product url': None,
#         'name': None,
#         'lego index': None,
#         'full media set': None,
#         'fixed size pics set': None
#     }

#     product_data['product url'] = page
#     product_data['name'] = get_product_name(page)
#     product_data['lego index'] = get_product_id(page)

#     time.sleep(10)

#     soup = get_data(page, headers=headers)
#     # data = soup.find_all('div', class_='ProductGallerystyles__MediaWrapper-sc-1uy048w-1 kBxAec')   
#     data = soup.find_all('picture', class_='ProductGallerystyles__StyledPicture-sc-1uy048w-4 yhckI')
#     for page in data:
#         result = page.find('source').get('srcset')
#         raw_mediaset.append(result)
#         for i in raw_mediaset:
#             media_urlset = i.split(', ')

#             for x in media_urlset:
#                 pic = x.split(' ')[0]
#                 product_media_urls.append(pic)  

#             for y in product_media_urls:
#                 if y[-3:] == '1.5':
#                     product_media_full_size_picture.append('y')

#     page_count += 1
#     print(page_count)
#     print(product_data)


#     product_data['full media set'] = product_media_urls
#     product_data['fixed size pics set'] = product_media_full_size_picture
#     full_products_data.append(product_data)
#     raw_mediaset.clear()
#     product_media_urls.clear()
#     product_media_full_size_picture.clear()  

# print(datetime.datetime.now())
# print(len(full_products_data))

# with open('data/products_data', 'a', encoding='utf-8') as file:
#     json.dump(full_products_data, file, indent=4, ensure_ascii=False)

