from flask import Flask, request
from flask import render_template
import pymysql
import os

import socket
import cv2
import numpy as np



# Socket Server [S] --------------------------------------- 
def recvall(sock, count):
    # 바이트 문자열
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

HOST = '192.168.0.162'
PORT = 8485

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')
s.bind((HOST, PORT))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')

conn, addr = s.accept()

length = recvall(conn, 16)
stringData = recvall(conn, int(length))
data = np.fromstring(stringData, dtype='uint8')
frame = cv2.imdecode(data, cv2.IMREAD_COLOR)
cv2.imwrite('Image.png', frame)
# Socket Server [E] --------------------------------------- 



# Food Classification (Yolov5) [S] --------------------------------------- 
# 음식 이름 정보 받아오기
food_eng_list = os.popen('python D:/dang/yolo/detect.py --weights "D:/dang/yolo/runs/train/exp3/weights/best.pt" --source "D:/dang/yolo/ttest/"').read() 
food_eng_list = food_eng_list.split('\n')
food_eng_list.pop()

image_path = food_eng_list[0].split('\\')
image_path = "D://dang/yolo/runs/detect/" + image_path[-1] + "/1.jpg"

print(image_path)
food_eng_list = food_eng_list[1:]
# Food Classification (Yolov5) [E] --------------------------------------- 



# 데이터 저장 리스트
food_data_list = []
food_name_list = []
male_total_nutrient = [130, 65, 54, 2600]
female_total_nutrient = [130, 55, 54, 2000]
food_first_weight = [219, 235, 63, 153]
food_last_weight = [29, 127, 5, 30]
food_weight = [food_first_weight[0]-food_last_weight[0], food_first_weight[1]-food_last_weight[1], food_first_weight[2]-food_last_weight[2], food_first_weight[3]-food_last_weight[3]]


male_avg = []
female_avg = []



# SQL Access (MariaDB) [S] --------------------------------------- 
# DB 접근 후 알맞은 데이터 추출
db = pymysql.connect(host='localhost', user='root', db='food', password='123456', charset='utf8')
curs = db.cursor()
 
for i in food_eng_list:
    name_sql = f"select food_name from foods where food_eng_name='{i}'";
    
    sql = f"select tan, dan, gi, cal from foods where food_eng_name='{i}'";
 
    curs.execute(sql)
    
    rows = curs.fetchall()
    food_data_list.append(rows)
    
    curs.execute(name_sql)
    
    rows = curs.fetchall()
    food_name_list.append(rows)
# SQL Access (MariaDB) [E] --------------------------------------- 



    
for i in range(4):
    male_avg.append( int((food_data_list[0][0][i] *food_weight[i]/100 + food_data_list[1][0][i]*food_weight[i]/100 + food_data_list[2][0][i]*food_weight[i]/100 + food_data_list[3][0][i]*food_weight[i]/100) / male_total_nutrient[i] * 100) )
    female_avg.append( int((food_data_list[0][0][i]*food_weight[i]/100 + food_data_list[1][0][i]*food_weight[i]/100 + food_data_list[2][0][i]*food_weight[i]/100 + food_data_list[3][0][i]*food_weight[i]/100) / female_total_nutrient[i] * 100) )

for i in range(4):
    if male_avg[i] > 100:
        male_avg[i] = 100
			
    if female_avg[i] > 100:
        female_avg[i] = 100
	
app = Flask(__name__) # 플라스크 어플리케이션 생성 코드

@app.route('/') # 특정 url에 접속하면 다음 줄에 있는 함수를 호출
def main():
	return render_template("index.html", food_data_list=food_data_list, food_name_list=food_name_list, male_avg=male_avg, female_avg=female_avg, image_path=image_path, food_weight=food_weight)

if __name__ == "__main__": # 직접 실행이면 웹 서버 실행
	app.run(host="0.0.0.0", port=5500, debug=False)