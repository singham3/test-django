from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import json
import re
import time
import threading

# drive = webdriver.Chrome('/home/lokesh/Downloads/chromedriver_linux64/chromedriver')
url = "https://www.alibaba.com/product-detail/Sandals-Baby-Wholesale-Infant-Fur-Summer_1600155557068.html?spm=a2700.galleryofferlist_catalog.normal_offer.d_image.5b071f1e2DOjWs&s=p"

req = requests.get(url)
soup = BeautifulSoup(req.content, 'html.parser')

product_details = soup.find_all('script', text=re.compile("globalData = "))
if len(product_details) > 0:
    details = json.loads(product_details[0].replace('</script>').split('window.detailData =')[-1])['globalData']['product']['price']['productBasicProperties']
    print(details)
else:
    print(product_details)

# cats = soup.find_all("h2")
# cat_list = []
#
#
# def get_sub_sub_cat(url):
#     inner_req = requests.get(url)
#     inner_soup = BeautifulSoup(inner_req.content, 'html.parser')
#     if 'did not match any products.' in inner_soup.prettify():
#         return []
#     category_data = inner_soup.find_all('script', text=re.compile(".*window.__page__data__config =.*"))
#     if len(category_data) > 0:
#         category_data = category_data[0].string.replace(
#             '<script>', ''
#             ).replace(
#             'window.__page__data__config =', ''
#         ).replace(
#             'window.__page__data = window.__page__data__config.props', ''
#         ).replace(
#             '</script>', ''
#         )
#         data = json.loads(category_data)
#         sub_sub_cats = []
#         for i in data['props']['snData']['category']['categoryGalleryData'][0]['values'][0]['childs'][0]['childs']:
#             sub_sub_cats.append(i['name'])
#         return sub_sub_cats
#     return []
#
#
# get_sub_sub_cat('https://www.alibaba.com/catalog/agricultural-waste_cid138')
# for cat in cats:
#     cat_dict = {cat.text: []}
#     for sub_cat in cat.findNext('ul'):
#         n = sub_cat.find('a')
#         n_dict = {}
#         if not isinstance(n, int):
#             print(n.text, 'https://www.alibaba.com/catalog' + n.get('href').lower().replace('pid', 'cid'))
#             n_dict[n.text] = get_sub_sub_cat('https://www.alibaba.com/catalog' + n.get('href').lower().replace('pid', 'cid'))
#             cat_dict[cat.text].append(n_dict)
#     cat_list.append(cat_dict)
#     open('test1.txt', 'w').write(str(cat_list))
#
# print(cat_list, len(cat_list))
