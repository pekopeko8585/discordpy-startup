from discord.ext import tasks, commands
import os
import discord
import datetime
import threading
import time
import sched
import asyncio

token = os.environ['DISCORD_BOT_TOKEN']

# 接続に必要なオブジェクトを生成
client = discord.Client()

#yggdrasil = [3,'21:00','ユグドラシル開店は本日22時です！']
#yggdrasil = [5,'03:45','ユグドラシル開店は本日22時です！']

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
    
    # メッセージを送る
    if message.content == '/remind':
        sendloop.start(message.channel)
        return

# 60秒に一回ループ
@tasks.loop(seconds=60)
async def sendloop(channel):
    # 0 1 2 3 4 5 6
    # 月火水木金土日
    # 現在の時刻
    d_today = datetime.datetime.now()
    await channel.send('テスト開始')
    
    with open('eventList.csv') as f:
        await channel.send('テスト1')
        file_data = f.readlines()
        await channel.send('テスト555')
        await channel.send(file_data)

        for item in file_data:
            await channel.send('テスト2')
            eventList.append(item)
            eventList.append(item.split(',')[0])
            
    await channel.send('テスト終了')
    
    for item in eventList:
        if  d_today.weekday() == item[0] and item[1] == d_today.strftime('%H:%M'):
            await channel.send(item[2])
    
# Botの起動とDiscordサーバーへの接続
client.run(token)
