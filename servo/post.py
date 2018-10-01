#coding:utf-8

import RPi.GPIO as GPIO
from requests_oauthlib import OAuth1Session
import json
from datetime import datetime
import time
from slacker import Slacker

try:
    with open('lock.txt',mode='x') as f:
        f.write('1')
except FileExistsError:
    pass


#slackの投稿の設定
# API token
token = 'hogehogehogehogheoghoeghoehgoehgoehgoehgoeh'
# 投稿するチャンネル名
c_name = 'example'
 # 投稿
slacker = Slacker(token)

#twitterの投稿の設定
CK = 'hogehogehoehgoehgoehgoehgoehgoe'                             # Consumer Key
CS = 'hogehogehogehogheoghoeghgoehgoehgoehgoehgoehgoehgoe'         # Consumer Secret
AT = 'heoghoeghoehgoehgoehgoehgoehgoehgoehgoehgoehgoehgoehgoehgoe' # Access Token
AS = 'hoeghoehgoehgoehgoehgoehgoehgoehgoehgoehgoehgoehgoe'         # Accesss Token Secert

# ツイート投稿用のURL
url = "https://api.twitter.com/1.1/statuses/update.json"
twitter = OAuth1Session(CK, CS, AT, AS)

time_stamp=datetime.now().strftime("%Y/%m/%d %H:%M:%S")

global lock
lock=0
auto=1

#サーボの設定
GPIO.setmode(GPIO.BOARD)

sw1_in=17
sw2_in=23
reed=21
GPIO.setup(sw1_in,GPIO.IN)
GPIO.setup(sw2_in,GPIO.IN)
GPIO.setup(reed,GPIO.IN)

led1_out=31 #赤
led2_out=22 #青
led3_out=26 #緑
GPIO.setup(led1_out,GPIO.OUT)
GPIO.setup(led2_out,GPIO.OUT)
GPIO.setup(led3_out,GPIO.OUT)

def open_key(): #鍵を開けるやつ
    time_stamp=datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    slacker.chat.post_message(c_name, '鍵開けて\n' + time_stamp, as_user=True)
    global lock
    lock=0
    print ("鍵を開けました。\n" + time_stamp)

def close_key():
    time_stamp=datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    slacker.chat.post_message(c_name, '鍵閉めて\n'+ time_stamp, as_user=True)
    
    global lock
    lock=1
    print ("鍵を閉めました\n" + time_stamp)

def LED():#LEDが光るだけのやつだから要らない
    GPIO.output(led3_out,0)
    GPIO.output(led1_out,0)
    GPIO.output(led2_out,0)

    GPIO.output(led1_out,1)
    time.sleep(1)
    GPIO.output(led1_out,0)
    GPIO.output(led2_out,1)
    time.sleep(1)
    GPIO.output(led2_out,0)
    GPIO.output(led3_out,1)
    time.sleep(1)
    GPIO.output(led3_out,0)
    GPIO.output(led1_out,1)
    GPIO.output(led2_out,1)

LED()
#Twitterに投稿
params = {"status": "起動しました。\n"+ time_stamp}
req = twitter.post(url, params = params)

try:
     while True:

        if GPIO.input(sw1_in)==1 and lock==1:
            open_key()

        elif GPIO.input(sw1_in)==1 and lock==0:
            close_key()

        elif GPIO.input(sw2_in)==1:
            #自動で閉まる
            GPIO.output(led1_out,0)
            GPIO.output(led2_out,0)
            GPIO.output(led3_out,1)
  
            while True:
                time.sleep(0.5)

                if GPIO.input(sw1_in)==1 and lock==1:
                    open_key()

                elif GPIO.input(sw1_in)==1 and lock==0:
                    close_key()

                elif GPIO.input(reed)==0 and auto==0:#開けたとき
                    auto=1

                elif GPIO.input(reed)==1 and auto==1: #閉めたとき
                    close_key()
                    auto=0

                elif GPIO.input(sw2_in)==1:
                    GPIO.output(led3_out,0)
                    break

                else :
                    auto=0
        else:

            pass
except KeyboardInterrupt:
    pass

servo.stop()
GPIO.cleanup()
