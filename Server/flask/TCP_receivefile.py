#TCP_receivefile.py
import socket
s_sock = socket.socket()
host = "localhost"
port = 2500
s_sock.connect((host, port)) #서버와 연결
s_sock.send("I am ready".encode()) #준비 완료 메시지 송신
fn = s_sock.recv(1024).decode()

with open('c:/Temp/'+fn, 'wb') as f: #저장 파일 열기
    print('file opened')
    print('receiving file...')
    while True:
        data = s_sock.recv(8192) #파일 내용 수신
        if not data: #내용이 없으면 종료
            break
        f.write(data)#내용을 파일에 쓰기
print('Download complete')
s_sock.close()
print('Connection closed')