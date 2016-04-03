#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys,hashlib,json
from pathlib import Path
from Crypto.Cipher import AES

class Upload:
  def __init__(self):
    self.limit = 20*1024*1024
    self.key = "zuSLNG5gzkHNvjPL"
    self.tmpdir = "/tmp"

  def encode(self,bary,BLOCK_SIZE):
    def pad(s,BLOCK_SIZE): 
      return s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * b"\0"
    cipher = AES.new(self.key)
    return cipher.encrypt(pad(bytes(bary),BLOCK_SIZE))

  def recv(self):
    bary_size = 0
    bary = bytearray()
    for buffer in sys.stdin.buffer:
      if bary_size+len(buffer) < self.limit:
        bary += buffer
        bary_size += len(buffer)
      else:
        yield bary
        bary = bytearray()
        bary_size = 0
    yield bary

  def create(self,func):
    self.fingerprints = []
    for self.bary in self.recv():
      self.enc = self.encode(self.bary,32)
      self.md5 = hashlib.md5(self.enc).hexdigest()
      self.p = Path(self.tmpdir,self.md5)
      with self.p.open("wb") as f:
        f.write(self.enc)
      func()
      self.fingerprints.append(self.md5)
    self.p = Path(self.tmpdir,"index.json")
    with self.p.open("w") as f:
      f.write(json.dumps(self.fingerprints))
      func()