#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cryptstream,argparse,subprocess,sys,hashlib,json
from pathlib import Path


parser = argparse.ArgumentParser(description="BaiduStreamer")
parser.add_argument('path',type=str)
parser.add_argument('--start',type=int)
parser.add_argument('--key')
args = parser.parse_args()

u = cryptstream.Upload()

if args.key:
  k = Path(args.key)
  if k.exists():
    with k.open("rb") as f:
      u.key = hashlib.md5(f.read()).hexdigest()

def byup():
  if (not u.p.name in files) or (files[u.p.name]["valid"] == False):
    proc = subprocess.Popen([
      "bypy",
      "upload",
      str(u.p),
      str( Path("/cryptstream/"+args.path) / u.p.name )
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    sys.stdout.write(proc[0].decode("utf-8"))
  u.p.unlink()

ls = subprocess.Popen([
  "bypy",
  "ls",
  str( Path("/cryptstream/"+args.path) )
], stdout=subprocess.PIPE, stderr=None).communicate()
files = {}
for line in ls[0].decode("utf-8").split("\n"):
  try:
    data = line.split(" ")
    files[data[1]] = {
      "size":data[2],
      "valid":(data[1]==data[5])
    }
  except:
    ""

u.create(post=byup,enc=hasattr(u,"key"))