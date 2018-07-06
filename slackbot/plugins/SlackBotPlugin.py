#coding:utf-8
from slackbot.bot import respond_to, listen_to
import re

import RPi.GPIO as GPIO
import time

#BOARDでpinで指定
GPIO.setmode(GPIO.BOARD)

global lock
lock=0

#PIN12を制御パルスの出力に設定
gp_out = 12
GPIO.setup(gp_out,GPIO.OUT)

led1_out=22 #赤
led2_out=24 #青
led3_out=26 #緑
GPIO.setup(led1_out,GPIO.OUT)
GPIO.setup(led2_out,GPIO.OUT)
GPIO.setup(led3_out,GPIO.OUT)

servo = GPIO.PWM(gp_out, 50)
servo.start(0)

def open(): #鍵を開けるやつ
    GPIO.setup(gp_out,GPIO.OUT)
    time.sleep(0.5)

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

servo.start(0)

#botの設定

# 「カギ開けて」「解錠して」等に反応するようにします
@listen_to(u'(鍵|カギ)+.*(開|あけ|空け)+')
@listen_to(u'(解錠)+')
@listen_to('(open)+.*(door)+')
@listen_to("(扉|とびら|トビラ)+.*(開|あけ|空け)+")
@listen_to("(開け|ひらけ|ヒラケ)+.*(塩|しお)")
def openKeyOrder(message, *something):
    if  lock==1:
        GPIO.output(led1_out,0)
        GPIO.output(led3_out,0)
        GPIO.output(led2_out,1)
        open()

        message.reply(u'わかりました。解錠します。')
        # 命令を出したユーザ名を取得することもできます。
        userID = message.channel._client.users[message.body['user']][u'name']
        print (userID + "さんの命令でカギを開けます")

    else:
        message.reply(u'鍵が開いているようです。')
        # 命令を出したユーザ名を取得することもできます。
        userID = message.channel._client.users[message.body['user']][u'name']
        print (userID + 'さんが鍵を開けようとしました。')

# 「鍵閉めて」「施錠」等の場合はこちら
@listen_to(u'(鍵|カギ)+.*(閉|しめ|締め)+')
@listen_to(u'(施錠)+')
@listen_to('(lock)+.*(door)+')
@listen_to("(扉|とびら|トビラ)+.*(閉|しめ|締め)+")
def closeKeyOrder(message, *something):
    if  lock==0:
        GPIO.output(led2_out,GPIO.LOW)
        GPIO.output(led1_out,GPIO.HIGH)
        GPIO.setup(gp_out,GPIO.OUT)
        close()

        message.reply(u'わかりました。施錠します。')
        # 命令を出したユーザ名を取得することもできます。
        userID = message.channel._client.users[message.body['user']][u'name']
        print (userID + "さんの命令でカギを閉めます")

    else:
        message.reply(u'鍵が閉まっているようです。')
        # 命令を出したユーザ名を取得することもできます。
        userID = message.channel._client.users[message.body['user']][u'name']
        print (userID + "さんが鍵を閉めようとしました。")
