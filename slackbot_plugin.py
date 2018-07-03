#coding:utf-8
# -*- coding: utf-8 -*-
from slackbot.bot import respond_to, listen_to
import re

import RPi.GPIO as GPIO
import time

#BOARDでpinで指定
GPIO.setmode(GPIO.BOARD)

#PIN12を制御パルスの出力に設定
gp_out = 12
GPIO.setup(gp_out,GPIO.OUT)

sw1_in=13
sw2_in=15
reed=19
GPIO.setup(sw1_in,GPIO.IN)
GPIO.setup(sw2_in,GPIO.IN)
GPIO.setup(reed,GPIO.IN)

led1_out=22 #赤
led2_out=24 #青
led3_out=26 #緑
GPIO.setup(led1_out,GPIO.OUT)
GPIO.setup(led2_out,GPIO.OUT)
GPIO.setup(led3_out,GPIO.OUT)

servo = GPIO.PWM(gp_out, 50)

#botの設定

# 「カギ開けて」「解錠して」等に反応するようにします
@listen_to(u'(鍵|カギ)+.*(開|あけ|空け)+')
@listen_to(u'(解錠)+')
@listen_to('(open)+.*(door)+', re.IGNORECASE)
@respond_to(u'(鍵|カギ)+.*(開|あけ|空け)+')
@respond_to(u'(解錠)+')
@respond_to('(open)+.*(door)+', re.IGNORECASE)
def openKeyOrder(message, *something):
    if  GPIO.output(led2_out)==GPIO.HIGH:
        GPIO.output(led1_out,GPIO.HIGH)
        servo.start(0)
        time.sleep(0.5)
        #デューティサイクルの値を変更することでサーボが回って角度が変わる。
        servo.ChangeDutyCycle(7.25)
        time.sleep(0.5)

        servo.ChangeDutyCycle(12)
        time.sleep(0.5)

        servo.ChangeDutyCycle(7.25)
        time.sleep(0.5)

        servo.stop()
        GPIO.cleanup(gp_out)

        message.reply(u'わかりました。解錠します。')
        # 命令を出したユーザ名を取得することもできます。
        userID = message.channel._client.users[message.body['user']][u'name']
        print userID + 'さんの命令でカギを開けます

    else:
        message.reply(u'鍵が開いているようです。')
        # 命令を出したユーザ名を取得することもできます。
        userID = message.channel._client.users[message.body['user']][u'name']
        print userID + 'さんが鍵を開けようとしました。'

# 「鍵閉めて」「施錠」等の場合はこちら
@listen_to(u'(鍵|カギ)+.*(閉|しめ|締め)+')
@listen_to(u'(施錠)+')
@listen_to('(lock)+.*(door)+', re.IGNORECASE)
@respond_to(u'(鍵|カギ)+.*(閉|しめ|締め)+')
@respond_to(u'(施錠)+')
@respond_to('(lock)+.*(door)+', re.IGNORECASE)
def closeKeyOrder(message, *something):
    if  GPIO.output(led3_out)==GPIO.HIGH:
        GPIO.setup(gp_out,GPIO.OUT)
        GPIO.output(led1_out,GPIO.HIGH)

        #デューティサイクルの値を変更することでサーボが回って角度が変わる。
        servo.ChangeDutyCycle(7.25)
        time.sleep(0.5)

        servo.ChangeDutyCycle(2.5)
        time.sleep(0.5)

        servo.ChangeDutyCycle(7.25)
        time.sleep(0.5)

        GPIO.cleanup(gp_out)

        message.reply(u'わかりました。施錠します。')
        # 命令を出したユーザ名を取得することもできます。
        userID = message.channel._client.users[message.body['user']][u'name']
        print userID + 'さんの命令でカギを閉めます

    else:
        message.reply(u'鍵が閉まっているようです。')
        # 命令を出したユーザ名を取得することもできます。
        userID = message.channel._client.users[message.body['user']][u'name']
        print userID + 'さんが鍵を閉めようとしました。'
