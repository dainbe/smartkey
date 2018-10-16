import RPi.GPIO as GPIO
import time

#BOARDでpinで指定
GPIO.setmode(GPIO.BOARD)

#PIN12を制御パルスの出力に設定
gp_out = 33
GPIO.setup(gp_out,GPIO.OUT)

led1_out=31 #赤
led2_out=22 #青
led3_out=26 #緑
GPIO.setup(led1_out,GPIO.OUT)
GPIO.setup(led2_out,GPIO.OUT)
GPIO.setup(led3_out,GPIO.OUT)

servo = GPIO.PWM(gp_out, 50)
servo.start(0)

try:
    with open('/home/pi/slackbot/lock.txt','x') as f:
        f.write('1')
except FileExistsError:
    pass

def open_key(): #鍵を開けるやつ

    with open('/home/pi/slackbot/lock.txt','w') as f:
        f.write('0')
    GPIO.setup(gp_out,GPIO.OUT)
    GPIO.output(led1_out,0)
    GPIO.output(led2_out,1)

    GPIO.setup(gp_out, GPIO.OUT)
    time.sleep(0.5)

    servo.ChangeDutyCycle(7.25)
    time.sleep(0.5)

    servo.ChangeDutyCycle(12)
    time.sleep(0.5)

    servo.ChangeDutyCycle(7.25)
    time.sleep(0.5)

    GPIO.cleanup(gp_out)

def close_key():  # 鍵を閉めるやつ

    with open('/home/pi/slackbot/lock.txt','w') as f:
        f.write('1')

    GPIO.setup(gp_out,GPIO.OUT)
    GPIO.output(led1_out,1)
    GPIO.output(led2_out,0)

    GPIO.setup(gp_out, GPIO.OUT)
    time.sleep(0.5)

    servo.ChangeDutyCycle(7.25)
    time.sleep(0.5)

    servo.ChangeDutyCycle(2.5)
    time.sleep(0.5)

    servo.ChangeDutyCycle(7.25)
    time.sleep(0.5)

    GPIO.cleanup(gp_out)
