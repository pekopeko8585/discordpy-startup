from discord.ext import commands
import os
import traceback
import discord
import datetime

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']

dt_now = datetime.datetime.now()

# 接続に必要なオブジェクトを生成
client = discord.Client()

@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
async def peko(ctx, arg):
    await ctx.send('引数は' + arg + 'です')

@bot.command()
async def システム日時(ctx):
    await ctx.send('システム日付は' + dt_now.strftime('%Y-%m-%d %H:%M:%S') + 'です')

bot.run(token)
