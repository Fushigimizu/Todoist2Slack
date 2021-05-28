# -*- coding: utf-8 -*-
import todoist
import requests
import datetime
import json
import os
import re
from dotenv import load_dotenv

#Load Settings
load_dotenv()

url = os.environ['SLACK_URL']
token = os.environ['TODOIST_TOKEN']

morning = 9 #朝
night = 21 #夜

today = str(datetime.date.today())
re_time = re.compile(today + 'T(\d\d\:\d\d)\:\d\d')
now = datetime.datetime.now()
api = todoist.api.TodoistAPI(token)
api.sync()

#タスクの取得
items = api.state['items']
todaysTask = [[],[],[],[]]

def parent(x_data):
    parentNames = ""
    if(x_data['parent_id']):
        parentData = api.items.get(x_data['parent_id'])
        rec = parent(parentData['item'])
        parentNames = rec + parentData['item']['content'] + " - "
    return parentNames

for x in items:
    if (x.data['due']):
        if(x.data['due']['date'].startswith(today)) & (x.data['checked'] == 0):
            parentNames = parent(x.data)
            priority = x.data['priority']
            time = ""
            timeGroup = re_time.search(x.data['due']['date'])
            if timeGroup:
                time = '[～' + str(timeGroup.group(1)) + ']'

            todaysTask[priority-1].append(time + parentNames + x.data['content'])
            
tasks = "---------------------------------------\n"  
for i in range(4):
    tasks += "優先度" + str(i+1) + "\n"
    if todaysTask[3-i] != []:
        tasks += "・" + "\n・".join(todaysTask[3-i])
    tasks += "\n---------------------------------------\n"


text = ""
#時間ごとに処理
if now.hour < morning:
    #朝
    text += "今日のタスクはこちらです。\n" + tasks + "\n今日も頑張りましょう！"
elif (now.hour >= morning) & (now.hour < night):
    #日中
    if todaysTask == []:
        text += "既に今日のタスクはすべて完了しました。"
    else:
        text += "現在残っているタスクはこちらです。\n"  + tasks
else:
    #就寝前
    if todaysTask == []:
        text += "今日はすべてのタスクを完了しました！えらい！"
    else:
        text += "今日は以下のタスクを終えられませんでした……\n" + tasks + "\n明日は頑張りましょう。"


request = requests.post(url, data=json.dumps({'text':text}), headers={'content-type': 'application/json'})
