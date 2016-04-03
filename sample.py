#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cryptstream,argparse,os,json,sys


parser = argparse.ArgumentParser(description="BaiduStreamer")
parser.add_argument('command', choices=["upload","download"])
parser.add_argument('name')
parser.add_argument('--start',type=int)
args = parser.parse_args()


u = cryptstream.Upload()
u.tmpdir = "/home/hisaruki/Desktop"
u.recv(["md5sum","$op"])

with open(os.path.join(u.tmpdir,"list.json"),"w") as f:
  f.write(json.dumps(u.fingerprints))