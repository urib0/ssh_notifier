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

    new = ssh_client_view.main()
    incr = {i:new[i] for i in new.keys() if i not in old.keys()}
    decr = {i:old[i] for i in old.keys() if i not in new.keys()}

    s = ""
    if 0 != len(incr):
      s = s+f"\n- join clients\n"
      for i in incr.keys():
        s = s+f"{i}:{incr[i]}\n"

    if 0 != len(decr):
      s = s+f"\n- leave clients\n"
      for i in decr.keys():
        s = s+f"{i}:{decr[i]}\n"

    # 増減があれば現在のクライアントを追加
    if 0 != len(s):
      s = s+f"\n- current clients\n"
      for i in new.keys():
        s = s+f"{i}:{new[i]}\n"
      s = s+"\n"
      print(s)

      # line送信
      send_message(conf["line_token"],s)

    old = new
    print(dt.datetime.now())
    time.sleep(conf["interval"])

if __name__ == "__main__":
  main()
