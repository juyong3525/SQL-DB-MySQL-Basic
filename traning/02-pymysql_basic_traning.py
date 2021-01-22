# 1. 라이브러기 가져오기
import pymysql

# 2. db 접속하기
db = pymysql.connect(host='localhost',
                     port=3306,
                     user='root',
                     passwd='?????',  # git에 push 하지 말 것
                     db='ecommerce',
                     charset='utf8')

# 3. 커서 가져오기
ecommerce = db.cursor()

# 4. SQL 문 만들기
# sql_drop = "DROP TABLE IF EXISTS product"
sql = """
        CREATE TABLE product (
        PRODUCT_CODE VARCHAR(20) NOT NULL,
        TITLE VARCHAR(200) NOT NULL,
        ORI_PRICE INT,
        DISCOUNT_PRICE INT,
        DISCOUNT_PERCENT INT,
        DELIVERY VARCHAR(2),
        PRIMARY KEY(PRODUCT_CODE)
    );
    """

# 5. SQL 구문 실행하기
ecommerce.execute(sql)

# 6. DB에 complete 하기
db.commit()

# 7. DB 연결 닫기
db.close()
