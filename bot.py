# coding: utf-8

import RPi.GPIO as GPIO
from slackbot.bot import Bot
import time
from slacker import Slacker
from slackbot_settings  import API_TOKEN
from servo_settings import open_key,close_key

# API token
token = API_TOKEN

# 投稿するチャンネル名
c_name = 'key'

#投稿
slacker = Slacker(token)
try:
    with open('/home/pi/slackbot/lock.txt',mode='x') as f:
        f.write('1')
except FileExistsError:
    pass


with open('/home/pi/slackbot/lock.txt','r') as f:
    for row in f:
        key=int(row.strip())
        lock=key

GPIO.setmode(GPIO.BOARD)

led1_out=31 #赤
led2_out=22 #青
led3_out=26 #緑
GPIO.setup(led1_out,GPIO.OUT)
GPIO.setup(led2_out,GPIO.OUT)
GPIO.setup(led3_out,GPIO.OUT)

time.sleep(3)

GPIO.output(led1_out,0)
GPIO.output(led2_out,0)
GPIO.output(led3_out,0)
time.sleep(0.5)

for i in range(2):
    GPIO.output(led2_out,1)
    time.sleep(0.5)
    GPIO.output(led2_out,0)
    time.sleep(0.5)

if lock==1:
    GPIO.output(led2_out,0)
    GPIO.output(led1_out,1)
else:
    GPIO.output(led2_out,1)

def check_button():
     while True:
            with open('/home/pi/slackbot/lock.txt',mode='r') as f:
                for row in f:
                    key=int(row.strip())
                    lock=key

            if GPIO.input(sw1_in)==1 and lock==1:
                open_key()

            elif GPIO.input(sw1_in)==1 and lock==0:
                close_key()

            elif GPIO.input(sw2_in)==0:
                GPIO.output(led3_out,0)
                time.sleep(0.5)

            elif GPIO.input(sw2_in)==1:
                #自動で閉まる
                GPIO.output(led3_out,1)
                time.sleep(0.5)

                if GPIO.input(reed)==0 and auto==0:#開けたとき
                    auto=1

                elif GPIO.input(reed)==1 and auto==1: #閉めたとき
                    close_key()
                    auto=0
                else :
                    auto=0
        else:

            pass

    servo.stop()
    GPIO.cleanup()


def main():
    bot = Bot()
    # ボタン監視用のスレッドを起動する
    th_me = threading.Thread(target=check_button, name="th_check_button")
    th_me.setDaemon(True)
    th_me.start()
    try:
        slacker.chat.post_message(c_name, '起動しました', as_user=True)
        # botを起動する
        bot.run()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    print('start slackbot')
    main()
