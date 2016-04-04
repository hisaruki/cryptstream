#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cryptstream,argparse,subprocess,sys


parser = argparse.ArgumentParser(description="BaiduStreamer")
parser.add_argument('name')
parser.add_argument('--start',type=int)
args = parser.parse_args()


u = cryptstream.Upload()
u.tmpdir = "/home/hisaruki/Desktop"
u.divide = 20*1024

def bypy():
  """
  proc = subprocess.Popen([
    "bypy",
    "upload",
    str(u.p)
  ], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
  sys.stdout.write(proc[0].decode("utf-8"))
  u.p.unlink()
  """
u.create(bypy,True)




