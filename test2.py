import json

with open('data/products_data.json', 'r') as file:
    product_urls = json.load(file)

result = []

def redirected_products_collector(product_urls_list, processed_list):
    for record in product_urls_list:
        if len(record['1 size pics set']) == 0:
            # print(len(record['1 size pics set']), len(record['2 size pics set']), len(record['3 size pics set']))
            processed_list.append(record['product url'])

redirected_products_collector(product_urls, result)

print(len(result))

with open('unprocessed_urls.json', 'w', encoding='utf-8') as list:
    json.dump(result, list, indent=4, ensure_ascii=False)