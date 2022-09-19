#!/usr/bin/env python3
import ssh_client_view
import time

def check_client():
  s = ""
  # 増えたクライアントを確認
  ret = {i:new[i] for i in new.keys() if i not in old.keys()}
  if 0 != len(ret):
    s = s+f"join clients"
    for i in ret.keys():
      s = s+f"\n{i}:{ret[i]}"

  # 減ったクライアントを確認
  ret = {i:old[i] for i in old.keys() if i not in new.keys()}
  if 0 != len(ret):
    s = s+f"\n\nleave clients"
    for i in ret.keys():
      s = s+f"\n{i}:{ret[i]}"

  return s

old = {}
while(True):
  new = ssh_client_view.main()
  ret = check_client()

  # 増減があれば現在のクライアントを追加
  if 0 != len(ret):
    ret = ret+f"\n\ncurrent clients"
    for i in new.keys():
      ret = ret+f"\n{i}:{new[i]}"
    ret = ret+"\n"
    print(ret)

  old = new
  time.sleep(5)
