from discord.ext import tasks, commands
import os
import discord
import datetime
import threading
import time
import sched
import asyncio
import traceback

###############################################################################################
#                                                                                             #
# 改修時はメモリに残しているイベントデータを/viewコメントで取得してから直してね！！！！              #
#                                                                                             #
###############################################################################################


token = os.environ['DISCORD_BOT_TOKEN']

# 接続に必要なオブジェクトを生成
client = discord.Client()

TUUCHI_CHANNEL_ID = 817245146771882014

ERROR_CHANNEL_ID = 820499967764332583

list100 = ['9','金','21:00','3Dボンバーマン大会']

eventList_week = [list100]
eventList_week.append('9 水 21:50 ユグドラシル'.split(' '))
eventList_week.append('9 木 22:00 関西弁集会'.split(' '))
eventList_week.append('9 木 22:00 VR方言酒場のまってら'.split(' '))
eventList_week.append('9 火 22:00 イケメン喫茶(ブラッコリーさん所))'.split(' '))
eventList_week.append('9 月 22:00 撮影の集い'.split(' '))
eventList_week.append('9 水 21:00 謎解きワールド巡り｢#謎めぐり｣'.split(' '))
eventList_week.append('9 木 21:00 初心者向けワールドツアー'.split(' '))
eventList_week.append('9 日 15:00 授乳Cafeキタリナ「ID:Hoshi_Lime」'.split(' '))

list200 = ['1900101','00:00','おばけの会']
eventList_day = [list200]

list300 = ['22:00','マイジュウ']
eventList_everyday = [list300]

w_list = ['月', '火', '水', '木', '金', '土', '日']

#定数宣言
help_addweek = (
    '/addweek：定期的に通知したいイベントを追加します。\n'
    + '　　　パラメータは「第X曜日」、「曜日」、「時間」、「メッセージ」を半角スペースを挟んで指定してください。\n'
    + '　　　第X曜日は数字1桁を、毎週の場合は9を入力してください。\n'
    + '　　　曜日は「月」～「金」で指定してください。\n'
    + '　　　時間は必ずHH:mm形式の半角の「:」含み5桁で指定してください。\n'
    + '　　　現状適当な数字入れても予定に入りますが動きません。チェックめんどいの。許して。\n'
    + '　　　例として第2水曜日の午前9時に「メッセージ」と表示する場合：/add 2 水 09:00 メッセージ\n'
)

help_addday = (
    '/addday：単発で通知したいイベントを追加します。\n'
    + '　　　パラメータは「日付」、「時間」、「メッセージ」を半角スペース区切りで指定してください。\n'
    + '　　　「日時」はyyyymmdd形式です。\n'
    + '　　　「時間」はhh:MM形式です。\n'
    + '　　　2020年10月15日14時20分に「メッセージ」と表示する場合：/addday 20201015 14:20 メッセージ\n'
)

help_addeveryday = (
    '/addeveryday：毎日通知したいイベントを追加します。\n'
    + '　　　パラメータは「時間」、「メッセージ」を半角スペース区切りで指定してください。\n'
    + '　　　「時間」はhh:MM形式です。\n'
    + '　　　毎日21時10分に「メッセージ」と表示する場合：/addeveryday 21:10 メッセージ\n'
)

help_removeweek = (
    '/removeweek：定期通知予定のイベントを削除します。\n'
    + '　　　パラメータは「ID」を半角スペースを挟んで指定してください。\n'
    + '　　　「ID」は/viewコマンドで確認できます。なお、INDEXをIDとしているため削除するたびにIDは変動します。\n'
    + '　　　よくわかんねーって人は削除するたびに/viewしてみてください。\n'
)

help_removeday = (
    '/removeday:単発通知予定のイベントを削除します。\n'
    + '　　　パラメータは「ID」を半角スペースを挟んで指定してください。\n'
    + '　　　「ID」は/viewコマンドで確認できます。なお、INDEXをIDとしているため削除するたびにIDは変動します。\n'
    + '　　　よくわかんねーって人は削除するたびに/viewしてみてください。\n'
)

help_removeeveryday = (
    '/removeeveryday:毎日通知予定のイベントを削除します。\n'
    + '　　　パラメータは「ID」を半角スペースを挟んで指定してください。\n'
    + '　　　「ID」は/viewコマンドで確認できます。なお、INDEXをIDとしているため削除するたびにIDは変動します。\n'
    + '　　　よくわかんねーって人は削除するたびに/viewしてみてください。\n'
)

# 起動時に動作する処理
@client.event
async def on_ready():
    try:
        tuuchi_channel = client.get_channel(TUUCHI_CHANNEL_ID)
        tuuchi_channel.send('サーバーが勝手に再起動しやがりました。')
        sendloop.start(tuuchi_channel)
    except Exception as e:
        error_channel = client.get_channel(ERROR_CHANNEL_ID)
        await error_channel.send(traceback.format_exc())
        
# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    try:
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
        
        # 通知を追加_単発
        if message.content[:7] == '/addday':
            if len(message.content) <= 8 or message.content[8:].strip().count(' ') != 2:
                await message.channel.send(help_addday)
                retutn
            
            newEventList = message.content[8:].split(' ')
            eventList_day.append(newEventList) 
            await message.channel.send('新しいイベントを追加しました。')
            await message.channel.send(newEventList)
            return
    
        # 通知を追加_毎日
        if message.content[:12] == '/addeveryday':
            if len(message.content) <= 13 or message.content[13:].strip().count(' ') != 1:
                await message.channel.send(help_addeveryday)
                retutn
            
            newEventList = message.content[13:].split(' ')
            eventList_everyday.append(newEventList) 
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
        
        # 通知を削除_単発
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
        
        # 通知を削除_毎日
        if message.content[:15] == '/removeeveryday':
            tempstr = ''
            if len(message.content) <= 16 or message.content[16:].strip().count(' ') != 0:
                await message.channel.send(help_removeeveryday)
                return
            remove_id = int(message.content[16:].strip())
            if remove_id > len(eventList_everyday):
                await message.channel.send('存在しないIDです。/viewコマンドでIDを確認してください。')
                return
        
            tempstr = str(eventList_everyday[remove_id])
            await message.channel.send('右記のイベントを削除します。：' + tempstr) 
            eventList_everyday.pop(remove_id)
            retutn
        
            # テスト
        if message.content == '/test':
            error_channel = client.get_channel(ERROR_CHANNEL_ID)
            await error_channel.send('testだよーん')
            return

        # 通知予定を表示
        if message.content == '/view':
            count = 0
            count_day = 0
            count_everyday = 0
            tempstr = ''
            tempstr2 = ''
            tempstr3 = ''
        
            for item in eventList_everyday:
                tempstr3 = tempstr3 + 'ID「' + str(count_everyday) + '」：' + ','.join(item) + '\n'
                count_everyday = count_everyday + 1
            if tempstr3 == '':
                tempstr3 = '毎日通知予定のイベントはありません。\n'
            else:
                tempstr3 = '毎日知予定のイベントは以下の通りです\n' + tempstr3
        
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
            
            await message.channel.send(tempstr3 + tempstr + tempstr2)
            return
    
        # ヘルプを表示
        if message.content == '/help':
            tempstr = ('概要：イベントの通知をするBOTです。\n'
                + '　　　曜日、時間、メッセージを指定して毎週決まった時刻に通知します。\n'
                + '↓↓↓↓↓↓↓↓↓↓↓↓↓↓コマンド一覧↓↓↓↓↓↓↓↓↓↓↓↓↓↓\n'
                + '/sysdate:現在のサーバー日時を表示します。\n'
                + '/neko：鳴きます。\n'
                + '/remind：通知処理を開始します。基本的に一回のみでOKなので再起動時以外使用しないでください。\n'
                + '/view：現在通知予定のイベントをすべて表示します。\n'
                + help_addweek
                + help_addday
                + help_addeveryday
                + help_removeweek
                + help_removeday
                + help_removeeveryday
            )
            await message.channel.send(tempstr)
            return
    except Exception as e:
        error_channel = client.get_channel(ERROR_CHANNEL_ID)
        await error_channel.send(traceback.format_exc())
        
# 60秒に一回ループ
@tasks.loop(seconds=60)
async def sendloop(channel):
    try:
        # 0 1 2 3 4 5 6
        # 月火水木金土日
        # 現在の時刻
        dt = datetime.datetime
        now_week = w_list[datetime.date.today().weekday()]
        d_today = dt.now()

        tempstr = ''
        isFirst = True

        #毎日通知
        for item in eventList_everyday:
            #日時が一致した場合
            item0 = datetime.datetime.strptime(item[0], '%H:%M')
            item0 = item0 + datetime.timedelta(minutes=-10)
            if item0.strftime('%H:%M') == d_today.strftime('%H:%M'):
                if isFirst == False:
                    tempstr = tempstr + '\n'
                tempstr = tempstr + item[1] + '\n'
                isFirst = False
    
        #定期通知
        for item in eventList_week:
            # 曜日と日時が一致した場合
            item2 = datetime.datetime.strptime(item[2], '%H:%M')
            item2 = item2 + datetime.timedelta(minutes=-10)
            if (item[0] == str(9) or item[0] == str(get_nth_week(datetime.date.today().day))) and now_week == item[1] and item2.strftime('%H:%M') == d_today.strftime('%H:%M'):
                if isFirst == False:
                    tempstr = tempstr + '\n'
                tempstr = tempstr + item[3] + '\n'
                isFirst = False

        #単発通知
        count = 0
        for item in eventList_day:
            # 日時が一致した場合
            item1 = datetime.datetime.strptime(item[1], '%H:%M')
            item1 = item1 + datetime.timedelta(minutes=-10)
            if item[0] == d_today.strftime('%Y%m%d') and item1.strftime('%H:%M') == d_today.strftime('%H:%M'):
                if isFirst == False:
                    tempstr = tempstr + '\n'
                tempstr = tempstr + item[2] + '\n'
                isFirst = False

                del eventList_day[count]
                count -= 1
            count += 1
    
        if tempstr != '':
            tempstr = '--------------10分後に下記イベントが行われます。--------------\n' + tempstr
            tuuchi_channel = client.get_channel(TUUCHI_CHANNEL_ID)
            await tuuchi_channel.send(tempstr)
    except Exception as e:
        error_channel = client.get_channel(ERROR_CHANNEL_ID)
        await error_channel.send('通知処理でエラーが発生しちゃったよ。')
        await error_channel.send(traceback.format_exc())

def get_nth_week(day):
    return (day - 1) // 7 + 1

def get_nth_dow(year, month, day):
    return get_nth_week(day), calendar.weekday(year, month, day)

# Botの起動とDiscordサーバーへの接続
client.run(token)
