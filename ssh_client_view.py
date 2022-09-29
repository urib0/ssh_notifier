#!/usr/bin/env python3
import os
import pprint
import subprocess

def main():
  try:
    with open(os.environ['HOME']+"/.ssh/authorized_keys", "r") as f:
      auth_key_list = f.readlines()
  except Exception as e:
    print(e)
    exit(0)

  # #permitlisten=127.0.0.1:{port} {host} を抜き出す
  comment_list = [i[:-1] for i in auth_key_list if i[:2] == "#p"]

  # port:hostの辞書を作る
  port_host_dic = {i.split(" ")[0].split(":")[1]:i.split(" ")[1] for i in comment_list if 1 < len(i.split(" "))}

  # listenしているポートのリストを作成
  cmd = 'ss -altn|grep -oE [0-9]{5}'
  port_list = subprocess.Popen(cmd, stdout=subprocess.PIPE,shell=True).communicate()[0].decode("utf-8").split("\n")[:-1]

  matched_port_list = sorted(set([i for i in port_list if i in port_host_dic.keys()]))
  matched_dic = {i:port_host_dic[i] for i in matched_port_list}
  return matched_dic

if __name__ == "__main__":
  ret = main()
  for i in ret:
    print(f"{i}:{ret[i]}")