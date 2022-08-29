import RPi.GPIO as GPIO 
import time


# button_callback function
def button_callback(channel):
    pass


button_pin = 15 # 사용할 GPIO핀의 번호 설정
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM) 
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # 버튼 핀의 IN/OUT 설정 , PULL DOWN 설정
 
GPIO.add_event_detect(button_pin,GPIO.RISING,callback=button_callback) # 신호 감지 시 button_callback 함수 실행

while 1:
    time.sleep(0.1) # 0.1초 딜레이