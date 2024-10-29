import time, datetime, json, requests
from bs4 import BeautifulSoup

headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

def get_data(url, headers):
    req = requests.get(url, headers=headers, allow_redirects=False)
    soup = BeautifulSoup(req.text, 'lxml')
    return soup

def get_product_name(url):
    product_name = ' '.join((url.split('/')[-1]).split('-')[:-1])
    return product_name

def get_product_id(url):
    product_id = (url.split('/')[-1]).split('-')[-1]
    return product_id

with open('unprocessed_urls.json', 'r') as file:
    product_urls = json.load(file)
print(product_urls)

print(datetime.datetime.now())

full_products_data = []
raw_mediaset = []
product_media_urls = []
product_media_3_size = []
product_media_2_size = []
product_media_1_size = []

page_count = 0
print(product_urls)
for page in product_urls:
    product_data = {
        'product url': None,
        'name': None,
        'lego index': None,
        '1 size pics set': None,
        '2 size pics set': None,
        '3 size pics set': None,
    }

    product_data['product url'] = page
    product_data['name'] = get_product_name(page)
    product_data['lego index'] = get_product_id(page)

    # time.sleep(10)

    soup = get_data(page, headers=headers)
    # data = soup.find_all('div', class_='ProductGallerystyles__MediaWrapper-sc-1uy048w-1 kBxAec')   
    data = soup.find_all('picture', class_='ProductGallerystyles__StyledPicture-sc-1uy048w-4 yhckI')
    for page in data:
        result = page.find('source').get('srcset')
        raw_mediaset.append(result)
        for i in raw_mediaset:
            media_urlset = i.split(', ')

            for x in media_urlset:
                pic = x.split(' ')[0]
                product_media_urls.append(pic)

            for y in product_media_urls:
                if y[-2:] == '=1':
                    product_media_1_size.append(y)

            for y in product_media_urls:
                if y[-2:] == '=3':
                    product_media_3_size.append(y)

            for y in product_media_urls:
                if y[-2:] == '=2':
                    product_media_2_size.append(y)
            

    page_count += 1
    print(page_count)

    # if page_count == 150:
    #     time.sleep(601)

    # if page_count == 300:
    #     time.sleep(300)

    # if page_count == 350:
    #     time.sleep(300)

    # if page_count == 500:
    #     time.sleep(300)

    # if page_count == 650:
    #     time.sleep(300)

    # if page_count == 900:
    #     time.sleep(300)

    # if page_count == 700:
    #     time.sleep(300)

    # if page_count == 800:
    #     time.sleep(300)

    # product_data['full media set'] = product_media_urls[0:5].copy()
    print(len(product_media_urls))
    product_data['1 size pics set'] = product_media_1_size[0:5].copy()
    product_data['2 size pics set'] = product_media_2_size[0:5].copy()
    product_data['3 size pics set'] = product_media_3_size[0:5].copy()

    full_products_data.append(product_data)
    print(product_data)
    raw_mediaset.clear()
    product_media_urls.clear()
    product_media_1_size.clear()  
    product_media_2_size.clear()
    product_media_3_size.clear()
    
print(datetime.datetime.now())
print(len(full_products_data))

with open('data/aditional_products_data.json', 'w', encoding='utf-8') as file:
    json.dump(full_products_data, file, indent=4, ensure_ascii=False)