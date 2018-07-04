#coding:utf-8

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

#PIN12を制御パルスの出力に設定
gp_out = 12
GPIO.setup(gp_out, GPIO.OUT)

global lock
auto=0 #オートロック用
lock=0 #0で開いてる１で閉まってる

#入力の設定
sw1_in=13
sw2_in=15
reed=21
GPIO.setup(sw1_in,GPIO.IN)
GPIO.setup(sw2_in,GPIO.IN)
GPIO.setup(reed,GPIO.IN)

#出力の設定
led1_out=22#赤
led2_out=24 #青
led3_out=26 #緑
GPIO.setup(led1_out,GPIO.OUT)
GPIO.setup(led2_out,GPIO.OUT)
GPIO.setup(led3_out,GPIO.OUT)

def open(): #鍵を開けるやつ
    GPIO.setup(gp_out,GPIO.OUT)
    time.sleep(0.5)
#自分の家の鍵はこの向きなので合わせて適宜変更を
    servo.ChangeDutyCycle(7.25)
    time.sleep(0.5)

    servo.ChangeDutyCycle(12)
    time.sleep(0.5)

    servo.ChangeDutyCycle(7.25)
    time.sleep(0.5)

    GPIO.cleanup(gp_out)
    global lock

    lock=0

def close(): #鍵を閉めるやつ
    GPIO.setup(gp_out,GPIO.OUT)
    time.sleep(0.5)

    servo.ChangeDutyCycle(7.25)
    time.sleep(0.5)

    servo.ChangeDutyCycle(2.5)
    time.sleep(0.5)

    servo.ChangeDutyCycle(7.25)
    time.sleep(0.5)

    GPIO.cleanup(gp_out)

    global lock
    lock=1

#GPIO.PWM( [ピン番号] , [周波数Hz] )
#PWMサイクル:20ms(=50Hz), 制御パルス:0.5ms〜2.4ms, (=2.5%〜12%)。
servo = GPIO.PWM(gp_out, 50)

#パルス出力開始。servo.start( [デューティサイクル 0~100%] )
servo.start(0)
#time.sleep(1)
try:
    while True:
        if GPIO.input(sw1_in)==1 and lock==1:
            GPIO.output(led1_out,0)
            GPIO.output(led3_out,0)

            GPIO.output(led2_out,1)

            open()

        elif GPIO.input(sw1_in)==1 and lock==0:
            GPIO.output(led2_out,0)
            GPIO.output(led3_out,0)

            GPIO.output(led1_out,1)

            close()

        elif GPIO.input(sw2_in)==1:
            #自動で閉まる
            GPIO.output(led1_out,0)
            GPIO.output(led2_out,0)
            GPIO.output(led3_out,1)

            while True:
                if GPIO.input(reed)==1:
                    if auto==0:
                        close()
                        auto=1

                    elif GPIO.input(sw1_in)==1 or GPIO.input(sw2_in)==1:
                        break
                else :
                    auto=0
        else:

            pass
except KeyboardInterrupt:
    pass

servo.stop()
GPIO.cleanup()
