from discord.ext import commands
import os
import traceback
import discord
import datetime
import threading
import time
import sched
import asyncio

token = os.environ['DISCORD_BOT_TOKEN']

# 接続に必要なオブジェクトを生成
client = discord.Client()

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

@client.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)

@tasks.loop(seconds=60)
async def loop():
    now = datetime.now().strftime('%H:%M')
    channel = client.get_channel('806529550355791872') #発言チャンネルを指定
    
    #12:00・18:00にニュースを自動取得する
    if now == '19：50' or now == '19:51' or now == '19:52' or now == '19:53' or now == '19:54' or now == '19:55' or now == '19:56':
        await channel.send('hoge')
        
# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    d_today = datetime.datetime.now()
    
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    
    await message.channel.send('きてるよ')
        
    # システム日付を返す。
    if message.content == '/sysdate':
        await message.channel.send('きてるよ2')
        await message.channel.send(d_today.strftime('%Y-%m-%d %H:%M:%S'))
        return
    
    # 「/neko」と発言したら「にゃーん」が返る処理
    if message.content == '/neko':
        await message.channel.send('にゃーん')
        return

    
# Botの起動とDiscordサーバーへの接続
client.run(token)
