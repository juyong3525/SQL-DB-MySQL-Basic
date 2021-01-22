import pymysql

db = pymysql.connect(
    host='localhost',
    user='root',
    passwd='killerqueen3525',   # git 에 push 하지 말 것
    db='yong',
    charset='utf8'
)

cursor = db.cursor()

sql = """
    select name, model_num, model_type from exercise
"""

cursor.execute(sql)
rows = cursor.fetchall()

for row in rows:
    print(row)


db.commit()
db.close()
