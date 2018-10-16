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
commander_token = #追加させるようのAPI,なくてもいい

smart_lock_ID = "スマートロックのID"
master_ID = "自分のID"

slacker = Slacker(token)

global lock

root_user = []
instant_user = []

try: #もしファイルがなかったらつくる。
    with open('/home/pi/slackbot/list.txt', mode='x') as f:
        f.write(master_ID)
except FileExistsError:
    pass

#root_userのリストに
with open("/home/pi/slackbot/list.txt","r") as f:
    for i in f:
        root_user.append(i.rstrip("\n"))

print (root_user)

#botの設定
@listen_to(u'(鍵|カギ|かぎ)+.*(開け|あけ|空け)+')
@respond_to(u'(鍵|カギ|かぎ)+.*(開け|あけ|空け)+')
@respond_to(u'(解錠)+')
@respond_to('(open)+.*(door)+')
@respond_to(u'(扉|トビラ|とびら)+.*(開け|あけ|空け)+')
@respond_to(u'(ひらけ|開け)+.*(ゴマ|ごま)+')
def openKeyOrder(message, *something):
    userID = message.channel._client.users[message.body['user']][u'id']
    userName =message.channel._client.users[message.body['user']][u'name']

    #message.reply(userName)
    my_attachments = {"fallback": "test", \
                      "actions": [{\
                                   "type": "button", \
                                   "text": "はい", \
                                   "url": "https://slack.com/api/chat.postMessage?token="+commander_token+"&channel="+smart_lock_ID+"&text=add%20%3C%40"+userID+"%3E%20instant&as_user=Ture&pretty=1"\
                                   },\
                                  {\
                                   "type": "button", \
                                   "text": "いいえ", \
                                   "url": "https://slack.com/api/chat.postMessage?token="+commander_token+"&channel="+smart_lock_ID+"&text=rm%20%3C%40"+userID+"%3E%20instant&as_user=Ture&pretty=1"}]}
    attachment = [my_attachments]

    if userID in root_user or userID in instant_user:
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
            slacker.chat.post_message(master_ID, userName + "さんの命令でカギを開けます。", as_user=True)


        else:
            message.reply(u'鍵が開いているようです。')

    else:
        message.reply("権限がありません。")
        slacker.chat.post_message(master_ID,'<@'+userID+'>さんが鍵を開けようとしました。\n許可しますか？', as_user=True,  attachments=attachment)

# 「鍵閉めて」「施錠」等の場合はこちら
@respond_to(u'(鍵|カギ)+.*(閉め|しめ|締め|占め)+')
@respond_to(u'(施錠)+')
@respond_to('(lock)+.*(door)+')
def closeKeyOrder(message, *something):
    userID = message.channel._client.users[message.body['user']][u'id']
    userName = message.channel._client.users[message.body['user']][u'name']
    #message.reply(userName)

    if userID in root_user or userID in instant_user:
        with open('/home/pi/slackbot/lock.txt',mode='r') as f:
            for row in f:
                key=int(row.strip())
                global lock
                lock=key
        if  lock==0:

            message.reply(u'わかりました。施錠します。')
            close_key()

            print (userName + "さんの命令でカギを閉めます。")
            slacker.chat.post_message(master_ID, userName + "さんの命令でカギを閉めます。", as_user=True)

        else:
            message.reply(u'鍵が閉まっているようです。')

    else:
        message.reply("権限がありません。")

@respond_to("add (.*) (.*)")
def add_list_order(message,user,add_list):
    userID = message.channel._client.users[message.body['user']][u'id']
    userName =message.channel._client.users[message.body['user']][u'name']
    add_user = user.replace("<@","").replace(">","")
    root = "root"
    if userID in root_user: #投稿者がrootかどうか
        if add_user in root_user or add_user in instant_user:#追加するユーザーがすでにいるか
            message.reply(user+"はすでに追加されているようです。")
            print(user+" already added")

        else:
            message.reply(add_list+"を"+user+"追加しました。")
            exec(add_list+"_user.append(add_user)")
            slacker.chat.post_message(add_user, add_list+'に追加されました。', as_user=True)
            print("instant_user = "+str(instant_user))
            print("root_user = "+str(root_user))

            if (root in add_list) ==True:
                with open('/home/pi/slackbot/list.txt', 'w')as f:
                    for i in root_user:
                        f.write(str(i) + "\n")
    else:
        message.reply("権限がありません。")

@respond_to("rm (.*) (.*)")
def rm_instant_order(message,user,rm_list):
    userID = message.channel._client.users[message.body['user']]['id']
    userName = message.channel._client.users[message.body['user']][u'name']
    rm_user = user.replace("<@","").replace(">","")
    root = "root"
    if userID in root_user:
        if rm_user in root_user or rm_user in instant_user:
            message.reply(rm_list+"を"+user+"から削除しました。")
            exec(rm_list+"_user.remove(rm_user)")
            slacker.chat.post_message(rm_user, rm_list+'から削除されました。', as_user=True)
            print("instant_user = "+str(instant_user))
            print("root_user = "+str(root_user))

            if (root in rm_list) ==True:
                with open('/home/pi/slackbot/list.txt', 'w')as f:
                    for i in root_user:
                        f.write(str(i) + "\n")

        else:
            message.reply(user+"は、すでに削除されているようです。")
            print(user+" already removed")
    else:
        message.reply("権限がありません。")
