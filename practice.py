from tkinter import *   # tk 모듈을 사용함
import threading
import RPi.GPIO as GPIO
import time


flag1 = True
flag2 = True
musicflag = True


# LED 포트번호
north = 26 


# 버저 포트 번호
buz = 4


# 불필요한 warning 제거,  GPIO핀의 번호 모드 설정

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# LED의 출력 설정

GPIO.setup(north, GPIO.OUT)

# BUZZER의 출력 설정
GPIO.setup(buz, GPIO.OUT)

# PWM 인스턴스 p를 만들고  GPIO 18번을 PWM 핀으로 설정, 주파수  = 100Hz
p = GPIO.PWM(buz, 100) 
Frq = [392, 392, 440, 440, 392, 392, 330, 
        392, 392, 330, 330, 294, 
        392, 392, 440, 440, 392, 392, 330,
        392, 330, 294, 330, 262]

speed = 0.5 # 음과 음 사이 연주시간 설정 (0.5초)
count = 0 # 음을 하나 연주했을때의 카운트

# 딜레이 시간 (센서 측정 간격)
delay = 0.5

gui_window = Tk() # 윈도우 객체를 하나 생성함.

def execute1():
    t1 = threading.Thread(target=sum, args=())
    t1.start()

def doit1():
    global flag1
    if flag1:
        flag1 = not flag1
        button1.config(text="Led On")
        GPIO.output(north, 1)

    else :
        flag1 = not flag1
        button1.config(text="Led Off")
        GPIO.output(north, 0) 

def doit2():
    global flag2
    global musicflag
    if flag2:
        flag2 = not flag2
        button2.config(text="Music On")
        if not musicflag :
            musicflag = True
        execute1()
        
    else :
        flag2 = not flag2
        musicflag = not musicflag
        execute1()
        button2.config(text="Music Off")

# Thread가 실행할 코드

def sum():
    global musicflag
    global count

    while True:
        if musicflag : 
            p.start(10)
            for fr in Frq:
                p.ChangeFrequency(fr)    #주파수를 fr로 변경
                time.sleep(speed)       #speed 초만큼 딜레이 (0.5s) 
                count += 1

                if count == 7:
                    time.sleep(speed * 2) # 1.0
                elif count == 12:
                    time.sleep(speed * 3) # 1.5
                elif count == 19:
                    time.sleep(speed * 2) # 1.0
            p.stop()
            
        else : 
            p.stop()
            break

    return

button1 = Button(gui_window, text = "LED OFF", command=doit1)
button1.pack()
button2 = Button(gui_window, text = "MUSIC OFF", command=doit2)
button2.pack()

gui_window.mainloop()