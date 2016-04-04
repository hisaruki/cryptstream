#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys,hashlib,json,base64
from pathlib import Path
from Crypto.Cipher import AES

class Upload:
  def __init__(self):
    self.divide = 20*1024*1024
    self.key = "zuSLNG5gzkHNvjPL"
    self.tmpdir = "/tmp"

  def AESenc(self,bary,BLOCK_SIZE):
    def pad(s,BLOCK_SIZE): 
      return s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * "{"
    cipher = AES.new(self.key)
    return cipher.encrypt(pad(base64.b64encode(bary).decode("utf-8"),BLOCK_SIZE))

  def recv(self):
    bary_size = 0
    bary = bytearray()
    for buffer in sys.stdin.buffer:
      if bary_size+len(buffer) < self.divide:
        bary += buffer
        bary_size += len(buffer)
      else:
        yield bary
        bary = bytearray()
        bary_size = 0
        bary += buffer
        bary_size += len(buffer)
    yield bary

  def create(self,pre=None,post=None,enc=True):
    self.fingerprints = []
    for bary in self.recv():
      self.file = bary
      if enc:
        self.file = self.AESenc(bary,32)
      self.md5 = hashlib.md5(self.file).hexdigest()
      self.p = Path(self.tmpdir,self.md5)
      if pre:pre()
      with self.p.open("wb") as f:
        f.write(self.file)
      if post:post()
      self.fingerprints.append(self.md5)
    self.p = Path(self.tmpdir,"index.json")
    if pre:pre()
    with self.p.open("w") as f:
      f.write(json.dumps(self.fingerprints))
    if post:post()

class Download:
  def __init__(self):
    self.key = "zuSLNG5gzkHNvjPL"
    self.tmpdir = "/tmp"

  def AESdec(self,bin):
    cipher = AES.new(self.key)
    return base64.b64decode(cipher.decrypt(bin))

  def create(self,pre=None,post=None,dec=True):
    self.p = Path(self.tmpdir,"index.json")
    if pre:pre()
    with self.p.open("r") as f:
      self.fingerprints = json.loads(f.read())
    if post:post()
    for fingerprint in self.fingerprints:
      self.p = Path(self.tmpdir,fingerprint)
      if pre:pre()
      with self.p.open("rb") as f:
        bin = f.read()
      self.file = bin
      if dec:
        self.file = self.AESdec(bin)
      if post:post()