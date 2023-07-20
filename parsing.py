import requests
from bs4 import BeautifulSoup as bs

headers = {
    'Accept': '*/*',
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}
q = {"key" : "macbook"}
site = requests.get(
    'https://asaxiy.uz/product/',
    headers=headers,params=q
)
htmldom = bs(site.text, 'lxml')
get_needed_div = htmldom.find_all('div', class_='product__item d-flex flex-column justify-content-between')
counter = 0
all_images = dict()
for aaaa in get_needed_div:
    counter += 1
    a =aaaa.find('a').get('href')
    all_images[f"product_{counter}"] = f"{a}"
print(all_images)

with open('search.html','w', encoding='UTF8') as file:
    file.write(site.text)
#
# with open('asaxiy.html', encoding='UTF8') as file:
#     html = file.read()
# #

# a = []
# get_needed_div = htmldom.find_all('div', class_='swiper-slide')
# counter = 0
# for aaaa in get_needed_div:
#     counter += 1
#     img_url = aaaa.find('img').get('data-src')
#     a.append(img_url)
# print(len(a))
# a.remove(None)
# print(a)
#
