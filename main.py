import todoist
import requests
import datetime
import json

url = "<Slack Incoming Webhook URL"
token = '<Todoist Token>'

today = str(datetime.date.today())
now = datetime.datetime.now()
api = todoist.api.TodoistAPI(token)
api.sync()

items = api.state['items']
todaysTask = []
for x in items:
    if (x.data['due'] != None):
        if(x.data['due']['date'] == today) & (x.data['checked'] == 0):
            todaysTask.append(x.data['content'])
            

tasks = "・" + "\n・".join(todaysTask)

text = ""
if now.hour < 9:
    #朝
    text += "今日のタスクはこちらです。\n" + tasks
elif (now.hour > 9) & (now.hour < 21):
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


request = requests.post(url, data=json.dumps({"text":text}), headers={'content-type': 'application/json'})