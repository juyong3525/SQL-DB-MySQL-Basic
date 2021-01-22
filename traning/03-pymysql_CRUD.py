import pymysql

db = pymysql.connect(host='localhost',
                     user='root',
                     passwd='?????',  # git에 push 하지 말 것
                     db='ecommerce',
                     charset='utf8')

cursor = db.cursor()

# INSERT
for index in range(10):
    product_code = str(637468341827621732 + index + 1)

    insert_sql = """
    insert into product values(
        '""" + product_code + """',
        '[이지바이]겨울베스트아이템균일가/후리스/패딩/자켓/조끼/기모',
        26300,
        7900,
        69,
        'F');
    """
    # cursor.execute(insert_sql)


# SELECT
select_sql = "select * from product"
cursor.execute(select_sql)
result = cursor.fetchall()

for record in result:
    print(record)


# 마지막 작업
db.commit()
db.close()
