from discord.ext import tasks, commands
import os
import discord
import datetime
import threading
import time
import sched
import asyncio

###############################################################################################
#                                                                                             #
# 改修時はメモリに残しているイベントデータを/viewコメントで取得してから直してね！！！！              #
#                                                                                             #
###############################################################################################


token = os.environ['DISCORD_BOT_TOKEN']

# 接続に必要なオブジェクトを生成
client = discord.Client()

yggdrasil = ['3','21:00','ユグドラシル開店は本日22時です！']

eventList = [yggdrasil]

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')
        
# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
        
    # システム日付を返す。
    if message.content == '/sysdate':
        d_today = datetime.datetime.now()
        await message.channel.send(d_today.strftime('%Y-%m-%d %H:%M:%S'))
        return
    
    # 「/neko」と発言したら「にゃーん」が返る処理
    if message.content == '/neko':
        await message.channel.send('にゃーん')
        return
    
    # 通知を開始
    if message.content == '/remind':
        sendloop.start(message.channel)
        return
    
    await message.channel.send(message.content[:5])
    # 通知を追加
    if message.content[:4] == '/add':
        if len(message.content) <= 5 or message.content[5:].strip().count(' ') != 2:
            await message.channel.send('パラメータは「曜日」、「時間」、「メッセージ」を半角スペースを挟んで指定してください。')
            await message.channel.send('水曜日の20時に「メッセージ」と表示する場合：/add 2 20:00 メッセージ')
            retutn
            
        newEventList = message.content[5:].split(' ')
        eventList.append(newEventList) 
        await message.channel.send('新しいイベントを追加しました。')
        await message.channel.send(newEventList)
        return
    
    # 通知を表示
    if message.content == '/view':
        for item in eventList:
            await message.channel.send(item)
        return
        
# 60秒に一回ループ
@tasks.loop(seconds=60)
async def sendloop(channel):
    # 0 1 2 3 4 5 6
    # 月火水木金土日
    # 現在の時刻
    d_today = datetime.datetime.now()
    
    for item in eventList:
        if  d_today.weekday() == item[0] and item[1] == d_today.strftime('%H:%M'):
            await channel.send(item[2])
    
# Botの起動とDiscordサーバーへの接続
client.run(token)
