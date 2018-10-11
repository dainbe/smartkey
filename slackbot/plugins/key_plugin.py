#coding:utf-8
from slackbot.bot import respond_to, listen_to
import re
import RPi.GPIO as GPIO
import time

import sys
sys.path.append('../')
from servo_settings import open_key,close_key

global lock

root_user = []
instant_user = []

with open("/home/pi/slackbot/list.txt","r") as f:
    for i in f:
        root_user.append(i.rstrip("\n"))

print (root_user)

#botの設定

@listen_to(u'(鍵|カギ)+.*(開け|あけ|空け)+')
@listen_to(u'(解錠)+')
@listen_to('(open)+.*(door)+')
def openKeyOrder(message, *something):
    userID = message.channel._client.users[message.body['user']][u'name']
    message.reply(userID)

    if userID in root_user or userID in instant_user:
        with open('/home/pi/slackbot/lock.txt',mode='r') as f:
            for row in f:
                key=int(row.strip())
                global lock
                lock=key
        if  lock==1:

            message.reply(u'わかりました。解錠します。')
            # 命令を出したユーザ名を取得することもできます。
            userID = message.channel._client.users[message.body['user']][u'name']

            open_key()

            print (userID + "さんの命令でカギを開けます")

        else:
            message.reply(u'鍵が開いているようです。')
            # 命令を出したユーザ名を取得することもできます。
            userID = message.channel._client.users[message.body['user']][u'name']
            print (userID + "さんが鍵を開けようとしました。")

    else:
        message.reply("You don't have permission")

# 「鍵閉めて」「施錠」等の場合はこちら
@listen_to(u'(鍵|カギ)+.*(閉め|しめ|締め|占め)+')
@listen_to(u'(施錠)+')
@listen_to('(lock)+.*(door)+')
def closeKeyOrder(message, *something):
    userID = message.channel._client.users[message.body['user']][u'name']
    message.reply(userID)

    if userID in root_user or userID in instant_user:
        with open('/home/pi/slackbot/lock.txt',mode='r') as f:
            for row in f:
                key=int(row.strip())
                global lock
                lock=key
        if  lock==0:

            message.reply(u'わかりました。施錠します。')
            # 命令を出したユーザ名を取得することもできます。
            userID = message.channel._client.users[message.body['user']][u'name']

            close_key()

            print (userID + "さんの命令でカギを閉めます")

        else:
            message.reply(u'鍵が閉まっているようです。')
            # 命令を出したユーザ名を取得することもできます。
            userID = message.channel._client.users[message.body['user']][u'name']
            print (userID + "さんが鍵を閉めようとしました。")

    else:
        message.reply("You don't have permission")

@listen_to("add (.*) to (.*)")
def add_list_order(message,user,add_list):
    userID = message.channel._client.users[message.body['user']][u'name']
    append_user = user
    root = "root"
    if userID in root_user: #投稿者がrootかどうか
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

@listen_to("rm (.*) to (.*)")
def rm_instant_order(message,user,rm_list):
    userID = message.channel._client.users[message.body['user']][u'name']
    rm_user = user
    root = "root"
    if userID in root_user:
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
