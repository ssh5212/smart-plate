import pymysql
 
db = pymysql.connect(host='localhost', user='root', db='food', password='123456', charset='utf8')
curs = db.cursor()
 
sql = "select * from foods";
print(type(sql))
 
curs.execute(sql)
 
rows = curs.fetchall()
print(rows)
 
db.commit()
db.close()