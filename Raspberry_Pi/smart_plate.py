import RPi.GPIO as GPIO 
import time
import picamera
import sys
from hx711 import HX711

import cv2
import socket
import numpy as np


# button_callback function
def button_callback(channel):
    # Camera Code [S] --------------------------------------- 
    camera = picamera.PiCamera()
    camera.resolution = (2592, 1944) # (64, 64) ~ (2592, 1944) px
    time.sleep(1)
    camera.capture('plate.jpg')
    # Camera Code [E] --------------------------------------- 

    # HX711 Code [S] --------------------------------------- 
    referenceUnit = 1

    def cleanAndExit():
        print("Cleaning...")
        GPIO.cleanup()
        print("Bye!")
        sys.exit()

    hx = HX711(5, 6)
    hx.set_reading_format("MSB", "MSB")
    hx.set_reference_unit(referenceUnit)
    hx.reset()

    print("Tare done! Add weight now...")

    # Socket Client Code [S] --------------------------------------- 
    try:
        val = hx.get_weight(5)
        print(val)
        hx.power_down()
        hx.power_up()
        time.sleep(0.1)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        s.connect(('192.168.0.162',8485))
    
        cam = cv2.imread('sajin2.png')
        
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        frame=cam
        result, frame = cv2.imencode('.jpg', frame, encode_param)
        data = np.array(frame)
        stringData = data.tostring()
        s.sendall((str(len(stringData))).encode().ljust(16) + stringData)
    # Socket Client Code [E] --------------------------------------- 
        
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
    # HX711 Code [E] --------------------------------------- 

# Button Code [S] --------------------------------------- 
button_pin = 15 # 사용할 GPIO핀의 번호 설정
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM) 
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # 버튼 핀의 IN/OUT 설정 , PULL DOWN 설정
 
GPIO.add_event_detect(button_pin,GPIO.RISING,callback=button_callback, bouncetime=300) # 신호 감지 시 button_callback 함수 실행

while 1:
    time.sleep(0.1) # 0.1초 딜레이
# Button Code [E] --------------------------------------- 