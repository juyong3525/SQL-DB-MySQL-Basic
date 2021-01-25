import pymysql


# DB 연결
host_name = 'localhost'
username = 'root'
password = 'killerqueen3525'    # git에 push하지 말 것
database_name = 'bestproducts'

db = pymysql.connect(
    host=host_name,
    user=username,
    passwd=password,
    db=database_name,
)
cursor = db.cursor()


def cursor_execute(sql):
    cursor.execute(sql)


def db_commit():
    db.commit()


def db_close():
    db.close()


def overlap_check(sql):
    cursor.execute(sql)
    result = cursor.fetchone()
    return result[0]
