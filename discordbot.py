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
        await message.channel.send(message.content)
        if len(message.content) <= 9 or message.content[9:].strip().count(' ') != 3:
            tempstr = 'パラメータは「第X曜日」、「曜日」、「時間」、「メッセージ」を半角スペースを挟んで指定してください。\n'
            tempstr = tempstr + '毎週水曜日の20時に「メッセージ」と表示する場合：/addweek 9 2 20:00 メッセージ'
            await message.channel.send(tempstr)
            retutn
        
        await message.channel.send(message.content[9:])
        newEventList = message.content[9:].split(' ')
        eventList_week.append(newEventList)
        await message.channel.send('新しいイベントを追加しました。')
        await message.channel.send(newEventList)
        return
        
    # 通知を追加_日時
    if message.content[:7] == '/addday':
        if len(message.content) <= 8 or message.content[8:].strip().count(' ') != 2:
            tempstr = 'パラメータは「日付」、「時間」、「メッセージ」を半角スペース区切りで指定してください。\n'
            tempstr = '「日時」はyyyy/mm/dd形式です。\n'
            tempstr = '「時間」はhh:MM形式です。\n'
            tempstr = tempstr + '2020年10月15日14時20分に「メッセージ」と表示する場合：/addday 2020/10/15 14:20 メッセージ'
            await message.channel.send(tempstr)
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
            tempstr = 'パラメータは「ID」を半角スペースを挟んで指定してください。\n'
            tempstr = tempstr + '「ID」は/viewコマンドで確認できます。なお、INDEXをIDとしているため削除するたびにIDは変動します。\n'
            tempstr = tempstr + 'よくわかんねーって人は削除するたびに/viewしてみてください。'
            await message.channel.send(tempstr)
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
            tempstr = 'パラメータは「ID」を半角スペースを挟んで指定してください。\n'
            tempstr = tempstr + '「ID」は/viewコマンドで確認できます。なお、INDEXをIDとしているため削除するたびにIDは変動します。\n'
            tempstr = tempstr + 'よくわかんねーって人は削除するたびに/viewしてみてください。'
            await message.channel.send(tempstr)
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
        await message.channel.send(type(eventList)) 
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
            tempstr = '毎週の通知予定のイベントはありません。\n'
        else:
            tempstr = '毎週の通知予定のイベントは以下の通りです\n' + tempstr
            
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
        tempstr = tempstr + '　　　曜日、時間、メッセージを指定して毎週決まった時刻に通知します。\n'
        tempstr = tempstr + '↓↓↓↓↓↓↓↓↓↓↓↓↓↓コマンド一覧↓↓↓↓↓↓↓↓↓↓↓↓↓↓\n'
        tempstr = tempstr + '/sysdate:現在のサーバー日時を表示します。\n'
        tempstr = tempstr + '/neko：鳴きます。\n'
        tempstr = tempstr + '/remind：通知処理を開始します。基本的に一回のみでOKなので再起動時以外使用しないでください。\n'
        tempstr = tempstr + '/view：現在通知予定のイベントをすべて表示します。\n'
        tempstr = tempstr + '/addweek：毎週通知したいイベントを追加します。\n'
        tempstr = tempstr + '　　　パラメータは「第X曜日」、「曜日」、「時間」、「メッセージ」を半角スペースを挟んで指定してください。\n'
        tempstr = tempstr + '　　　、曜日は月曜が0、火曜日が1～～～日曜日が6と数字で指定してください。\n'
        tempstr = tempstr + '　　　時間は必ずHH:mm形式の半角の「:」含み5桁で指定してください。\n'
        tempstr = tempstr + '　　　現状適当な数字入れても予定に入りますが動きません。チェックめんどいの。許して。\n'
        tempstr = tempstr + '　　　例として水曜日の午前9時に「メッセージ」と表示する場合：/add 2 09:00 メッセージ\n'
        tempstr = tempstr + '/removeweek：通知予定のイベントを削除します。\n'
        tempstr = tempstr + '　　　パラメータは「ID」を半角スペースを挟んで指定してください。\n'
        tempstr = tempstr + '　　　「ID」は/viewコマンドで確認できます。なお、INDEXをIDとしているため削除するたびにIDは変動します。\n'
        tempstr = tempstr + '　　　よくわかんねーって人は削除するたびに/viewしてみてください。'
        await message.channel.send(tempstr)
        return
        
# 60秒に一回ループ
@tasks.loop(seconds=60)
async def sendloop(channel):
    # 0 1 2 3 4 5 6
    # 月火水木金土日
    # 現在の時刻
    d_today = datetime.datetime.now()
    for item in eventList_week:
        # 曜日と日時が一致した場合
        if str(d_today.weekday()) == str(item[1]) and str(item[2]) == d_today.strftime('%H:%M'):
            await channel.send('きたよ1')
            if str(item[0]) == '9' or str(item[0]) == get_nth_week(d_today.strftime('%Y'),d_today.strftime('%m'),d_today.strftime('%D')):
                await channel.send('きたよ2')
                tempstr = '★★★★★★★★★★★★イベントのお知らせ★★★★★★★★★★★★\n'
                tempstr = tempstr + str(item[2]) + '\n'
                tempstr = tempstr + '★★★★★★★★★★★★イベントのお知らせ★★★★★★★★★★★★'
                await channel.send(tempstr)
                #eventList_week.remove(item)
            
def get_nth_week(day):
    return (day - 1) // 7 + 1

def get_nth_dow(year, month, day):
    return get_nth_week(day), calendar.weekday(year, month, day)



# Botの起動とDiscordサーバーへの接続
client.run(token)
