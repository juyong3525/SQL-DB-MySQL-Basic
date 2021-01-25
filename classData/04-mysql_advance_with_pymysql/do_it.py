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

        if ori_price == None or ori_price.get_text() == '':
            ori_price = dis_price

        if dis_price == None:
            ori_price, dis_price = 0, 0

        else:
            ori_price = ori_price.get_text().replace(',', '').replace('원', '')
            dis_price = dis_price.get_text().replace(',', '').replace('원', '')

        if discount_percent == None or discount_percent.get_text() == '':
            discount_percent = 0
        else:
            discount_percent = discount_percent.get_text().replace('%', '')

        product_link = item.select_one('div.thumb > a')
        item_code = product_link['href'].split('=')[1].split('&')[0]

        res = requests.get(product_link['href'])
        soup = BeautifulSoup(res.content, 'html.parser')
        provider = soup.select_one(
            'div.item-topinfo_headline p.shoptit span.text__seller > a')
        if provider == None:
            provider = ''
        else:
            provider = provider.get_text()

        print(category_name, sub_category_name, ranking, item_code,
              provider, title.get_text(), ori_price, dis_price, discount_percent)


# main/sub category 정보 가져오기
def get_category(category_link, category_name):
    res = requests.get(category_link)
    soup = BeautifulSoup(res.content, 'html.parser')

    get_items(soup, category_name, "ALL")

    sub_categories = soup.select('div.cate-l div.navi.group ul li > a')
    for sub_category in sub_categories:
        res = requests.get(
            'http://corners.gmarket.co.kr/' + sub_category['href'])
        soup = BeautifulSoup(res.content, 'html.parser')
        get_items(soup, category_name, sub_category.get_text())


# main 카테고리 가져오기
res = requests.get('http://corners.gmarket.co.kr/Bestsellers')
soup = BeautifulSoup(res.content, 'html.parser')

categories = soup.select('div.gbest-cate ul.by-group li a')
for category in categories:
    get_category('http://corners.gmarket.co.kr/' +
                 category['href'], category.get_text())
