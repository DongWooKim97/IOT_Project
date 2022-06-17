#!/usr/bin/env python
from flask import Flask, render_template, Response
from camera import Camera
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
SERVO_PIN = 26
ALARM_PIN = 18
flag = 0

GPIO.setup(PUSH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(ALARM_PIN, GPIO.OUT)

servo = GPIO.PWM(SERVO_PIN, 50)
servo.start(0)

app = Flask(__name__)
@app.route('/')
def index():
   return render_template('index.html')

def gen(camera):
   while True:
       frame = camera.get_frame()
       yield (b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_on')
def video_on():
    return Response(gen(Camera()),mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/door/on')
def door_on():
    global flag
    try:
        if flag == 0:
            GPIO.setup(SERVO_PIN, GPIO.OUT)
            servo.ChangeDutyCycle(12.5)
            flag = flag + 1
            time.sleep(2)
            GPIO.setup(SERVO_PIN, GPIO.IN)
            return "ok"
    except:
        servo.stop()
        GPIO.cleanup(SERVO_PIN)
        return "fail"

@app.route('/door/close')
def door_close():
    global flag
    try:
        if flag == 1:
            GPIO.setup(SERVO_PIN, GPIO.OUT)
            servo.ChangeDutyCycle(7.5)
            flag = flag -1
            time.sleep(2)
            GPIO.setup(SERVO_PIN, GPIO.IN)
            return "ok"
    except:
        servo.stop()
        GPIO.cleanup(SERVO_PIN)
        return "fail"


@app.route('/ring/on')
def ring_on():
    Frq = [262,294,330,349,392,440,493,523]
    speed = 0.5
    p = GPIO.PWM(18,100)
    try:
        while 1:
            p.start(10)
            for i in Frq:
                p.ChangeFrequency(i)
                time.sleep(speed)

            return "ok"
    except:
        servo.stop()
        GPIO.cleanup(ALARM_PIN)
        return "fail"



if __name__ == '__main__':
   app.run(host='0.0.0.0', debug=True, threaded=True)