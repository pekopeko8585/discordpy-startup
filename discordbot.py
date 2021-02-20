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
eventList_week = [yggdrasil]

yggdrasil2 = ['2020401','21:00','21時から飲み会やります！']
eventList_day = [yggdrasil2]

w_list = ['月', '火', '水', '木', '金', '土', '日']

#定数宣言
help_addweek = (
    '/addweek：定期的に通知したいイベントを追加します。\n'
    + '　　　パラメータは「第X曜日」、「曜日」、「時間」、「メッセージ」を半角スペースを挟んで指定してください。\n'
    + '　　　曜日は「月」～「金」、または「毎週」と指定してください。\n'
    + '　　　時間は必ずHH:mm形式の半角の「:」含み5桁で指定してください。\n'
    + '　　　現状適当な数字入れても予定に入りますが動きません。チェックめんどいの。許して。\n'
    + '　　　例として第2水曜日の午前9時に「メッセージ」と表示する場合：/add 2 水 09:00 メッセージ\n'
)

help_addday = (
    'パラメータは「日付」、「時間」、「メッセージ」を半角スペース区切りで指定してください。\n'
    + '「日時」はyyyy/mm/dd形式です。\n'
    + '「時間」はhh:MM形式です。\n'
    + '2020年10月15日14時20分に「メッセージ」と表示する場合：/addday 2020/10/15 14:20 メッセージ\n'
)

help_removeweek = (
    '/removeweek：通知予定のイベントを削除します。\n'
    + '　　　パラメータは「ID」を半角スペースを挟んで指定してください。\n'
    + '　　　「ID」は/viewコマンドで確認できます。なお、INDEXをIDとしているため削除するたびにIDは変動します。\n'
    + '　　　よくわかんねーって人は削除するたびに/viewしてみてください。\n'
)

help_removeday = (
    'パラメータは「ID」を半角スペースを挟んで指定してください。\n'
    + '「ID」は/viewコマンドで確認できます。なお、INDEXをIDとしているため削除するたびにIDは変動します。\n'
    + 'よくわかんねーって人は削除するたびに/viewしてみてください。\n'
)

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
        await message.channel.send('これより登録されているイベントを指定時間に通知します。')
        sendloop.start(message.channel)
        return
    
    # 通知を追加_週間
    if message.content[:8] == '/addweek':
        if len(message.content) <= 9 or message.content[9:].strip().count(' ') != 3:
            await message.channel.send(help_addweek)
            retutn
        
        newEventList = message.content[9:].split(' ')
        eventList_week.append(newEventList)
        await message.channel.send('新しいイベントを追加しました。')
        await message.channel.send(newEventList)
        return
        
    # 通知を追加_日時
    if message.content[:7] == '/addday':
        if len(message.content) <= 8 or message.content[8:].strip().count(' ') != 2:
            await message.channel.send(help_addday)
            retutn
            
        newEventList = message.content[8:].split(' ')
        eventList_day.append(newEventList) 
        await message.channel.send('新しいイベントを追加しました。')
        await message.channel.send(newEventList)
        return
    
    # 通知を削除_週間
    if message.content[:11] == '/removeweek':
        tempstr = ''
        if len(message.content) <= 12 or message.content[12:].strip().count(' ') != 0:
            await message.channel.send(help_removeweek)
            return
        remove_id = int(message.content[12:].strip())
        if remove_id > len(eventList_week):
            await message.channel.send('存在しないIDです。/viewコマンドでIDを確認してください。')
            return
        
        tempstr = str(eventList_week[remove_id])
        await message.channel.send('右記のイベントを削除します。：' + tempstr) 
        eventList_week.pop(remove_id)
        retutn
        
    # 通知を削除_日時
    if message.content[:10] == '/removeday':
        tempstr = ''
        if len(message.content) <= 11 or message.content[11:].strip().count(' ') != 0:
            await message.channel.send(help_removeday)
            return
        remove_id = int(message.content[11:].strip())
        if remove_id > len(eventList_day):
            await message.channel.send('存在しないIDです。/viewコマンドでIDを確認してください。')
            return
        
        tempstr = str(eventList_day[remove_id])
        await message.channel.send('右記のイベントを削除します。：' + tempstr) 
        eventList_day.pop(remove_id)
        retutn
        
        # テスト
    if message.content == '/test':
        await message.channel.send('testですver5')
        retutn

    # 通知を表示
    if message.content == '/view':
        count = 0
        count_day = 0
        tempstr = ''
        tempstr2 = ''
        for item in eventList_week:
            tempstr = tempstr + 'ID「' + str(count) + '」：' + ','.join(item) + '\n'
            count = count + 1
        if tempstr == '':
            tempstr = '定期通知予定のイベントはありません。\n'
        else:
            tempstr = '定期知予定のイベントは以下の通りです\n' + tempstr
            
        for item in eventList_day:
            tempstr2 = tempstr2 + 'ID「' + str(count_day) + '」：' + ','.join(item) + '\n'
            count_day = count_day + 1

        if tempstr2 == '':
            tempstr2 = '単発の通知予定のイベントはありません。'
        else:
            tempstr2 = '単発の通知予定のイベントは以下の通りです\n' + tempstr2
            
        await message.channel.send(tempstr + tempstr2)
        return
    
    # ヘルプを表示
    if message.content == '/help':
        tempstr = '概要：イベントの通知をするBOTです。\n'
        + '　　　曜日、時間、メッセージを指定して毎週決まった時刻に通知します。\n'
        + '↓↓↓↓↓↓↓↓↓↓↓↓↓↓コマンド一覧↓↓↓↓↓↓↓↓↓↓↓↓↓↓\n'
        + '/sysdate:現在のサーバー日時を表示します。\n'
        + '/neko：鳴きます。\n'
        + '/remind：通知処理を開始します。基本的に一回のみでOKなので再起動時以外使用しないでください。\n'
        + '/view：現在通知予定のイベントをすべて表示します。\n'
        + help_addweek
        + help_addday
        + help_removeweek
        + help_removeday
        await message.channel.send(tempstr)
        return
        
# 60秒に一回ループ
@tasks.loop(seconds=60)
async def sendloop(channel):
    # 0 1 2 3 4 5 6
    # 月火水木金土日
    # 現在の時刻
    dt = datetime.datetime
    now_week = w_list[datetime.date.today().weekday()]
    d_today = dt.now()
    await channel.send('topなうです6')
    #await channel.send(now_week)
    #await channel.send(item[1])

    for item in eventList_week:
        # 曜日と日時が一致した場合

        await channel.send('1つ目' + now_week + '：' + item[1])
        await channel.send('2つ目' + d_today.strftime('%H:%M'))

        if now_week == item[1] and item[2] == d_today.strftime('%H:%M'):
            await channel.send(now_week)
            #await channel.send(item[0])
            #await channel.send(int(d_today.strftime('%Y')))
            #await channel.send(int(d_today.strftime('%m')))
            #await channel.send(int(d_today.strftime('%d')))
            #await channel.send(get_nth_week(int(d_today.strftime('%Y')),int(d_today.strftime('%m')),int(d_today.strftime('%d'))))
            if item[0] == '毎週' or item[0] == now_week:
                await channel.send('きたよ2')
                tempstr = '★★★★★★★★★★★★イベントのお知らせ★★★★★★★★★★★★\n'
                tempstr = tempstr + item[2] + '\n'
                tempstr = tempstr + '★★★★★★★★★★★★イベントのお知らせ★★★★★★★★★★★★'
                await channel.send(tempstr)
                #eventList_week.remove(item)

    await channel.send('ループ終わった！')

def get_nth_week(day):
    return (day - 1) // 7 + 1

def get_nth_dow(year, month, day):
    return get_nth_week(day), calendar.weekday(year, month, day)

# Botの起動とDiscordサーバーへの接続
client.run(token)
