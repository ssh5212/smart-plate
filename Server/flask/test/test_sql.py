import pymysql

food_eng_list = ['yuggaejang', 'baegmi', 'mumallaengi', 'mechulial']

db = pymysql.connect(host='localhost', user='root', db='food', password='123456', charset='utf8')
curs = db.cursor()
 
food_data_list = []
food_name_list = []

for i in food_eng_list:
    name_sql = f"select food_name from foods where food_eng_name='{i}'";
    
    sql = f"select tan, dan, gi, cal from foods where food_eng_name='{i}'";
 
    curs.execute(sql)
    
    rows = curs.fetchall()
    food_data_list.append(rows)
    
    curs.execute(name_sql)
    
    rows = curs.fetchall()
    food_name_list.append(rows)
    

print(food_data_list[1][0][0])
print(food_data_list[2][0][1])
print(food_data_list[3][0][2])
print(food_name_list[1][0][0])

 
db.commit()
db.close()