import socket

# import sys
# if (len(sys.argv) > 1):
#     ServerIp = sys.argv[1]
# else:
#     print("Error")
#     exit(1)

ServerIp = "192.168.0.160"
PORT = 9898

s = socket.socket()
s.connect((ServerIp, PORT))

file = open("data.txt", "rb")
SendData = file.read(1024)


while SendData:
    print("Below message is received from server\n", s.recv(1024).decode('utf-8'))
    s.send(SendData)
    SendData = file.read(1024)

s.close()