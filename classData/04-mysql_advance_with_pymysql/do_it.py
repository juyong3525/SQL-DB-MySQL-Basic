import requests
from bs4 import BeautifulSoup


# 상품 정보 가져오기
def get_items(html, category_name, sub_category_name):
    items_result_list = list()

    best_item = html.select('div.best-list')
    for index, item in enumerate(best_item[1].select('li')):

        ranking = index + 1
        title = item.select_one('a.itemname')
        ori_price = item.select_one('div.o-price')
        dis_price = item.select_one('div.s-price strong span')
        discount_percent = item.select_one('div.s-price em')


# main/sub category 정보 가져오기
def get_category(category_link, category_name):
    # print(category_link, category_name)
    res = requests.get(category_link)
    soup = BeautifulSoup(res.content, 'html.parser')

    sub_categories = soup.select('div.cate-l div.navi.group ul li a')
    for sub_category in sub_categories:
        # print(category_link, category_name, sub_category.get_text(), 'http://corners.gmarket.co.kr/' +
        #       sub_category['href'])
        get_items(soup, category_name, sub_category.get_text())


# main 카테고리 가져오기
res = requests.get('http://corners.gmarket.co.kr/Bestsellers')
soup = BeautifulSoup(res.content, 'html.parser')

categories = soup.select('div.gbest-cate ul.by-group li a')
for category in categories:
    get_category('http://corners.gmarket.co.kr/' +
                 category['href'], category.get_text())
