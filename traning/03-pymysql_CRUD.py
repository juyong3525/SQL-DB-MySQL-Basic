import pymysql
import pandas as pd

db = pymysql.connect(host='localhost',
                     user='root',
                     passwd='?????',  # git에 push 하지 말 것
                     db='ecommerce',
                     charset='utf8')

cursor = db.cursor()


'''
# INSERT
for index in range(10):
    product_code = str(637468341827621732 + index + 1)

    insert_sql = f"""
    insert into product values(
        '{product_code}',
        '[이지바이]겨울베스트아이템균일가/후리스/패딩/자켓/조끼/기모',
        26300,
        7900,
        69,
        'F');
    """
    cursor.execute(insert_sql)
'''


'''
# SELECT
select_sql = "select * from product"
cursor.execute(select_sql)
result = cursor.fetchall()

for record in result:
    print(record)
'''


'''
# UPDATE
update_sql = """
update product set 
    PRODUCT_CODE='1517019865',
    TITLE='메이킹유 니트원피스/블라우스/맨투맨/코트 빅사이즈',
    ORI_PRICE=33000,
    DISCOUNT_PRICE=9900,
    DISCOUNT_PERCENT=70,
    DELIVERY='F'
    where PRODUCT_CODE = '637468341827621733'
"""

cursor.execute(update_sql)
'''

'''
# DELETE
delete_sql = """
delete from product 
    where PRODUCT_CODE = '637468341827621742'
"""

cursor.execute(delete_sql)
'''


# 마지막 작업
db.commit()
db.close()
