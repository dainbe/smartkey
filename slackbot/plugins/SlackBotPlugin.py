# coding:utf-8
from slackbot.bot import respond_to, listen_to
import re
import RPi.GPIO as GPIO
import time

global lock

try:
    with open('lock.txt', mode='x') as f:
        f.write('1')
except FileExistsError:
    pass

# BOARDでpinで指定
GPIO.setmode(GPIO.BOARD)

# PIN12を制御パルスの出力に設定
gp_out = 12
GPIO.setup(gp_out, GPIO.OUT)

sw1_in = 13
sw2_in = 19
reed = 21
GPIO.setup(sw1_in, GPIO.IN)
GPIO.setup(sw2_in, GPIO.IN)
GPIO.setup(reed, GPIO.IN)

led1_out = 15  # 赤
led2_out = 16  # 青
led3_out = 18  # 緑
GPIO.setup(led1_out, GPIO.OUT)
GPIO.setup(led2_out, GPIO.OUT)
GPIO.setup(led3_out, GPIO.OUT)

servo = GPIO.PWM(gp_out, 50)


def open_key():  # 鍵を開けるやつ
    GPIO.setup(gp_out, GPIO.OUT)
    time.sleep(0.5)

    servo.ChangeDutyCycle(7.25)
    time.sleep(0.5)

    servo.ChangeDutyCycle(12)
    time.sleep(0.5)

    servo.ChangeDutyCycle(7.25)
    time.sleep(0.5)

    GPIO.cleanup(gp_out)

    with open('lock.txt', mode='w') as f:
        f.write('0')


def close_key():  # 鍵を閉めるやつ
    GPIO.setup(gp_out, GPIO.OUT)
    time.sleep(0.5)

    servo.ChangeDutyCycle(7.25)
    time.sleep(0.5)

    servo.ChangeDutyCycle(2.5)
    time.sleep(0.5)

    servo.ChangeDutyCycle(7.25)
    time.sleep(0.5)

    GPIO.cleanup(gp_out)

    with open('lock.txt', mode='w') as f:
        f.write('1')

# botの設定

# 「カギ開けて」「解錠して」等に反応するようにします


@listen_to(u'(鍵|カギ)+.*(開|あけ|空け)+')
@listen_to(u'(解錠)+')
@listen_to('(open)+.*(door)+')
@listen_to("(扉|トビラ|とびら)+.*(開|あけ|空け)+")
def openKeyOrder(message, *something):
    with open('lock.txt', mode='r') as f:
        for row in f:
            key = int(row.strip())
            print(key)
            global lock
            lock = key

    if lock == 1:
        GPIO.output(led1_out, 0)
        GPIO.output(led3_out, 0)
        GPIO.output(led2_out, 1)
        open_key()

        message.reply(u'わかりました。解錠します。')
        # 命令を出したユーザ名を取得することもできます。
        userID = message.channel._client.users[message.body['user']][u'name']
        print(userID + "さんの命令でカギを開けます")

    else:
        message.reply(u'鍵が開いているようです。')
        # 命令を出したユーザ名を取得することもできます。
        userID = message.channel._client.users[message.body['user']][u'name']
        print(userID + 'さんが鍵を開けようとしました。')

# 「鍵閉めて」「施錠」等の場合はこちら


@listen_to(u'(鍵|カギ)+.*(閉|しめ|締め)+')
@listen_to(u'(施錠)+')
@listen_to('(lock)+.*(door)+')
def closeKeyOrder(message, *something):
    with open('lock.txt', mode='r') as f:
        for row in f:
            key = int(row.strip())
            print(key)
            global lock
            lock = key

    if lock == 0:
        GPIO.output(led2_out, GPIO.LOW)
        GPIO.output(led1_out, GPIO.HIGH)
        GPIO.setup(gp_out, GPIO.OUT)
        close_key()

        message.reply(u'わかりました。施錠します。')
        # 命令を出したユーザ名を取得することもできます。
        userID = message.channel._client.users[message.body['user']][u'name']
        print(userID + "さんの命令でカギを閉めます")

    else:
        message.reply(u'鍵が閉まっているようです。')
        # 命令を出したユーザ名を取得することもできます。
        userID = message.channel._client.users[message.body['user']][u'name']
        print(userID + "さんが鍵を閉めようとしました。")

