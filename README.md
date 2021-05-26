# Todoist2Slack
Todoist にあるその日のタスクを Slack に投稿します。時間帯によってメッセージを分けています。

# 事前準備
- 実行環境で todoist-python と requests と dotenv をインストールする
- Slack で Incoming Webhook を設定する
- Todoistのトークンを取得する
- .envを作る(後述)
- morning と night の値を必要に応じて変更する(後述)

# .env
  .envというファイルをmain.pyと同じディレクトリに作り、以下のように書き込みます。
  
  SLACK_URL=<Slack の Incoming Webhook URL>
  TODOIST_TOKEN=<Todoist のトークン>
  
# morning と night
このスクリプトは朝・日中・就寝前でメッセージを変えるようになっています。具体的には、時刻が morning より前なら朝のメッセージ、morning とnight の間なら日中のメッセージ、night 以降なら就寝前のメッセージが送信されます。そのため、実際に動かす時間に合わせてこれらの変数の値を変えてください。指定は時間単位です。
作者の場合は8:30, 10:00, 13:00, 16:00, 20:00, 22:00 に動かしているため、初期値は morning が9、night が21となっています。
なお、日中には morning の時間は含みますが night の時間は含みません。初期値の場合、9時台は日中ですが21時台は日中ではありません(はずです)。
