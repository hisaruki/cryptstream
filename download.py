#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cryptstream,argparse,subprocess,sys
from pathlib import Path

parser = argparse.ArgumentParser(description="BaiduStreamer")
parser.add_argument('path')
parser.add_argument('--start',type=int)
args = parser.parse_args()


d = cryptstream.Download()
d.tmpdir = "/home/hisaruki/Desktop"

def bydown():
  if not d.p.exists():
    frm = str( Path("/cryptstream/"+args.path) / d.p.name )
    print(frm)
    proc = subprocess.Popen([
      "bypy",
      "download",
      frm,
      d.tmpdir
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

def rm():
  d.p.unlink()

d.create(pre=bydown,post=rm,dec=True)