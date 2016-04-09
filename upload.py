#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cryptstream,argparse,subprocess,sys,hashlib
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
  dst = str( Path("/cryptstream/"+args.path) / u.p.name )
  proc = subprocess.Popen([
    "bypy",
    "upload",
    str(u.p),
    dst
  ], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
  sys.stdout.write(proc[0].decode("utf-8"))
  u.p.unlink()

u.create(post=byup,enc=hasattr(u,"key"))
