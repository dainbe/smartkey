#coding:utf-8

import RPi.GPIO as GPIO
from requests_oauthlib import OAuth1Session
import json
from datetime import datetime
import time
from slacker import Slacker

#slackの投稿の設定
# API token
token = 'xoxb-386763726407-394291088848-HLNeCbSAJVsnXJ03NcuoqSJG'
# 投稿するチャンネル名
c_name = 'key'
 # 投稿
slacker = Slacker(token)

#twitterの投稿の設定
CK = 'RhCTEfNAVUoZwCpDapJnZ3TsH'                             # Consumer Key
CS = 'YfumXXu2u6RaBWOQlmd6TZiNekT9zyFaY8DcS5nME7GqjmMaM7'         # Consumer Secret
AT = '923461717081833472-aUACpf7aWK1cQsXUvSOYm174NkmdGaQ' # Access Token
AS = 'hwzRTimcfVt50is8MJp2ZraR4YZHRZjllYu9rFsxXyIpw'         # Accesss Token Secert

# ツイート投稿用のURL
url = "https://api.twitter.com/1.1/statuses/update.json"

twitter = OAuth1Session(CK, CS, AT, AS)
time_stamp=datetime.now().strftime("%Y/%m/%d %H:%M:%S")

#サーボの設定
GPIO.setmode(GPIO.BOARD)

def open(): #鍵を開けるやつ
    time_stamp=datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    slacker.chat.post_message(c_name, '鍵開けて\n' + time_stamp, as_user=True)
    global lock
    lock=0
    print ("鍵を開けました。\n" + time_stamp)

def close():
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
            open()

        elif GPIO.input(sw1_in)==1 and lock==0:
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
