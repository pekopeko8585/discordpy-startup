from discord.ext import commands
import os
import discord
import datetime
import threading
import time
import sched
import asyncio
from discord.ext import tasks

token = os.environ['DISCORD_BOT_TOKEN']

# 接続に必要なオブジェクトを生成
client = discord.Client()
channel = client.get_channel('806529550355791872')

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')
        
# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    d_today = datetime.datetime.now()
    
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    
    await message.channel.send('きてるよ2')
        
    # システム日付を返す。
    if message.content == '/sysdate':
        await message.channel.send('きてるよ2')
        await message.channel.send(d_today.strftime('%Y-%m-%d %H:%M:%S'))
        return
    
    # 「/neko」と発言したら「にゃーん」が返る処理
    if message.content == '/neko':
        await message.channel.send('にゃーん')
        return

# 60秒に一回ループ
@tasks.loop(seconds=60)
async def loop():
    # 現在の時刻
     now = datetime.now().strftime('%H:%M')
     await channel.send(now)  
        
loop.start()
    
# Botの起動とDiscordサーバーへの接続
client.run(token)
