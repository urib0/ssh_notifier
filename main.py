#!/usr/bin/env python3
import ssh_client_view
import time
import json
import requests
import datetime as dt

def send_message(token,message):
    headers = {
        "Authorization": "Bearer " + token,
    }
    files = {
        "message": (None, message),
    }
    res = requests.post("https://notify-api.line.me/api/notify", headers=headers, files=files)
    return res

def main():
  old = {}
  while(True):
    # 設定読み込み
    with open("./config.json", "r") as f:
      conf = json.loads(f.read())

    # 現在のクライアントを取得
    new = ssh_client_view.main()

    msg = ""

    # クライアントが増えていればメッセージに追加
    incr = {i:new[i] for i in new.keys() if i not in old.keys()}
    if 0 != len(incr):
      msg = msg+f"\n- join clients\n"
      msg = msg+"".join([f"{i}:{incr[i]}\n" for i in incr.keys()])

    # クライアントが減っていればメッセージに追加
    decr = {i:old[i] for i in old.keys() if i not in new.keys()}
    if 0 != len(decr):
      msg = msg+f"\n- leave clients\n"
      msg = msg+"".join([f"{i}:{decr[i]}\n" for i in decr.keys()])

    # 増減があれば現在のクライアントを追加
    if 0 != len(msg):
      msg = msg+f"\n- current clients\n"
      msg = msg+"".join([f"{i}:{new[i]}\n" for i in new.keys()])

      # line送信
      send_message(conf["line_token"],msg)
      print(msg)

    old = new
    print(dt.datetime.now())
    time.sleep(conf["interval"])

if __name__ == "__main__":
  main()
