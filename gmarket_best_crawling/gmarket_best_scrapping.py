import requests
from bs4 import BeautifulSoup
from db_management import cursor_execute, db_commit, db_close, overlap_check


# db에 저장하기
def save_data(item_info):
    count_sql = f"""SELECT COUNT(*) FROM items WHERE item_code = '{item_info['item_code']}';"""
    overlap_num = overlap_check(count_sql)
    if overlap_num == 0:
        items_sql = f"""INSERT INTO items VALUES(
            '{item_info['item_code']}',
            '{item_info['title']}',
            {item_info['ori_price']},
            {item_info['dis_price']},
            {item_info['discount_percent']},
            '{item_info['provider']}'
        )
        """
        cursor_execute(items_sql)

    ranking_sql = f"""INSERT INTO ranking (main_category, sub_category, item_ranking, item_code) VALUES(
    '{item_info['category_name']}',
    '{item_info['sub_category_name']}',
    '{str(item_info['ranking'])}',
    '{item_info['item_code']}'
    )"""
    cursor_execute(ranking_sql)

    db_commit()
    global commited_num
    commited_num += 1
    print(f"{commited_num} commited")


# 판매 업체 정보 가져오기
def get_provider(link):
    try:
        res = requests.get(link)
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, 'html.parser')
            provider = soup.select_one(
                'div.item-topinfo_headline p.shoptit span.text__seller > a')
            if provider == None:
                provider = ''
            else:
                provider = provider.get_text()
            return provider
    except TimeoutError:
        pass


# 상품 정보 가져오기
def get_items(html, category_name, sub_category_name):
    best_item = html.select('div.best-list')
    for index, item in enumerate(best_item[1].select('li')):

        data_dict = dict()

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

        provider = get_provider(product_link['href'])
        if provider is None:
            provider = ''

        data_dict['category_name'] = category_name
        data_dict['sub_category_name'] = sub_category_name
        data_dict['ranking'] = ranking
        data_dict['title'] = title.get_text()
        data_dict['ori_price'] = ori_price
        data_dict['dis_price'] = dis_price
        data_dict['discount_percent'] = discount_percent
        data_dict['item_code'] = item_code
        data_dict['provider'] = provider

        save_data(data_dict)


# main/sub category 정보 가져오기
def get_category(category_link, category_name):
    try:
        res = requests.get(category_link)
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, 'html.parser')
            get_items(soup, category_name, "ALL")
            sub_categories = soup.select('div.cate-l div.navi.group ul li > a')
            for sub_category in sub_categories:
                try:
                    res = requests.get(
                        'http://corners.gmarket.co.kr/' + sub_category['href'])
                    if res.status_code == 200:
                        soup = BeautifulSoup(res.content, 'html.parser')
                        get_items(soup, category_name, sub_category.get_text())
                except TimeoutError:
                    pass
    except TimeoutError:
        pass


# main 카테고리 가져오기
def get_main_category():
    try:
        res = requests.get('http://corners.gmarket.co.kr/Bestsellers')
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, 'html.parser')
            categories = soup.select('div.gbest-cate ul.by-group li a')
            for category in categories:
                link = 'http://corners.gmarket.co.kr/' + category['href']
                get_category(link, category.get_text())
    except TimeoutError:
        pass


# 실행 함수
def main():
    global commited_num
    commited_num = 0
    get_main_category()
    db_close()
