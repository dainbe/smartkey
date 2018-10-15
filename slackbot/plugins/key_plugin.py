#coding:utf-8
from slackbot.bot import respond_to, listen_to
import re
import RPi.GPIO as GPIO
from slacker import Slacker
import sys
sys.path.append('../')
from servo_settings import open_key,close_key
from slackbot_settings import API_TOKEN

token = API_TOKEN
master_name = "自分のuserID"
slacker = Slacker(token)

global lock

root_user = []
instant_user = []

try: #もしファイルがなかったらつくる。
    with open('/home/pi/slackbot/list.txt', mode='x') as f:
        f.write('自分のuserName')
except FileExistsError:
    pass

#root_userのリストに
with open("/home/pi/slackbot/list.txt","r") as f:
    for i in f:
        root_user.append(i.rstrip("\n"))

print (root_user)

#botの設定

@respond_to(u'(鍵|カギ|かぎ)+.*(開け|あけ|空け)+')
@respond_to(u'(解錠)+')
@respond_to('(open)+.*(door)+')
@respond_to(u'(扉|トビラ|とびら)+.*(開け|あけ|空け)+')
@respond_to(u'(ひらけ|開け)+.*(ゴマ|ごま)+')
def openKeyOrder(message, *something):
    userName = message.channel._client.users[message.body['user']][u'name']
    #message.reply(userName)

    if userName in root_user or userName in instant_user:
        with open('/home/pi/slackbot/lock.txt',mode='r') as f:
            for row in f:
                key=int(row.strip())
                global lock
                lock=key
        if  lock==1:

            message.reply(u'わかりました。解錠します。')
            open_key()

            print (userName + "さんの命令でカギを開けます。")
            #自分あてに通知
            slacker.chat.post_message(master_name, userName + "さんの命令でカギを開けます。", as_user=True)


        else:
            message.reply(u'鍵が開いているようです。')

    else:
        message.reply("You don't have permission")
        slacker.chat.post_message(master_name, userName + "さんが鍵を開けようとしました。", as_user=True)

# 「鍵閉めて」「施錠」等の場合はこちら
@respond_to(u'(鍵|カギ)+.*(閉め|しめ|締め|占め)+')
@respond_to(u'(施錠)+')
@respond_to('(lock)+.*(door)+')
def closeKeyOrder(message, *something):
    userName = message.channel._client.users[message.body['user']][u'name']
    #message.reply(userName)

    if userName in root_user or userName in instant_user:
        with open('/home/pi/slackbot/lock.txt',mode='r') as f:
            for row in f:
                key=int(row.strip())
                global lock
                lock=key
        if  lock==0:

            message.reply(u'わかりました。施錠します。')
            close_key()

            print (userName + "さんの命令でカギを閉めます。")
            slacker.chat.post_message(master_name, userName + "さんの命令でカギを閉めます。", as_user=True)

        else:
            message.reply(u'鍵が閉まっているようです。')

    else:
        message.reply("You don't have permission")
        slacker.chat.post_message(master_name, userName + "さんが鍵を閉めようとしました。", as_user=True)

@respond_to("add (.*) to (.*)")
def add_list_order(message,user,add_list):
    userName = message.channel._client.users[message.body['user']][u'name']
    append_user = user
    root = "root"
    if userName in root_user: #投稿者がrootかどうか
        if append_user in root_user:#追加するユーザーがすでにいるか
            message.reply(user+" already added")

        else:
            message.reply("added "+add_list+" to "+user)
            exec(add_list+"_user.append(append_user)")

            if (root in add_list) ==True:
                with open('/home/pi/slackbot/list.txt', 'w')as f:
                    for i in root_user:
                        f.write(str(i) + "\n")
                print("root_user = "+str(root_user))
    else:
        message.reply("You don't have permission")

@respond_to("rm (.*) to (.*)")
def rm_instant_order(message,user,rm_list):
    userName = message.channel._client.users[message.body['user']][u'name']
    rm_user = user
    root = "root"
    if userName in root_user:
        if rm_user in root_user:
            message.reply("removed "+rm_list+" to "+user)
            exec(rm_list+"_user.remove(rm_user)")

            if (root in rm_list) ==True:
                with open('/home/pi/slackbot/list.txt', 'w')as f:
                    for i in root_user:
                        f.write(str(i) + "\n")
                print("root_user = "+str(root_user))

        else:
            message.reply(user+" already removed")

    else:
        message.reply("You don't have permission")
