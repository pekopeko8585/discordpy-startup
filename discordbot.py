from discord.ext import commands
import os
import traceback
import discord
import datetime

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
    
# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    d_today = datetime.date.today()
    
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    
    await message.channel.send('きてるよ')
        
    # システム日付を返す。
    if message.content == '/sysdate':
        await message.channel.send('きてるよ2')
        await message.channel.send(d_today.strptime('%Y/%m/%d %H:%M'))
        return
    
    # 「/neko」と発言したら「にゃーん」が返る処理
    if message.content == '/neko':
        await message.channel.send('にゃーん')
        return

    
# Botの起動とDiscordサーバーへの接続
client.run(token)
