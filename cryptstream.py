#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys,hashlib,os
from Crypto.Cipher import AES

class Upload:
  def __init__(self):
    self.limit = 20*1024*1024
    self.fingerprints = []
    self.tmpdir = "/tmp"
    self.key = "zuSLNG5gzkHNvjPL"

  def encode(self,data,BLOCK_SIZE):
    def pad(s,BLOCK_SIZE): 
      return s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * b"\0"
    cipher = AES.new(self.key)
    return cipher.encrypt(pad(data,BLOCK_SIZE))

  def tmp_write(self,bary):
    bary = self.encode(bytes(bary),32)
    fingerprint = hashlib.md5(bary).hexdigest()
    self.fingerprints.append(fingerprint)
    with open(os.path.join(self.tmpdir,fingerprint),"wb") as f:
      f.write(bary)

  def recv(self):
    bary_size = 0
    bary = bytearray()
    for buffer in sys.stdin.buffer:
      if bary_size+len(buffer) < self.limit:
        bary += buffer
        bary_size += len(buffer)
      else:
        self.tmp_write(bary)
        bary = bytearray()
        bary_size = 0
    self.tmp_write(bary)
