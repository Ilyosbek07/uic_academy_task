import requests
from bs4 import BeautifulSoup as bs


def product_detail(product_name):
    headers = {
        'Accept': '*/*',
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    site = requests.get(
        f'https://asaxiy.uz/uz{product_name}',
        headers=headers
    )
    #
    product_dict = {}
    htmldom = bs(site.text, 'html.parser')
    price = htmldom.find_all('span', class_='price-box_new-price')[0]['content']
    name = htmldom.find('li', class_='breadcrumb-item active').text
    img_url = htmldom.find_all('a', class_='swiper-slide item__main-img')[0]['href']
    description = htmldom.find('div', class_='description__item').find('p').text[:201]
    product_dict['price'] = price
    product_dict['name'] = name
    product_dict['img_url'] = img_url
    product_dict['description'] = description
    product_dict['url'] = product_name
    return product_dict
# with open('detail.html','w', encoding='UTF8') as file:
#     file.write(site.text)
#
# with open('detail.html', encoding='UTF8') as file:
#     html = file.read()

# htmldom = bs(html, 'lxml')
