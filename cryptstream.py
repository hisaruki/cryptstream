#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys,hashlib,json
from pathlib import Path
from Crypto.Cipher import AES

class Upload:
  def __init__(self):
    self.divide = 20*1024*1024
    self.tmpdir = "/tmp"

  def AESenc(self,bary,BLOCK_SIZE):
    def pad(s,BLOCK_SIZE): 
      return s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * b"\0", (BLOCK_SIZE - len(s) % BLOCK_SIZE)
    cipher = AES.new(self.key)
    bin,pad = pad(bytes(bary),BLOCK_SIZE)
    return cipher.encrypt(bin),pad

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

  def create(self,pre=None,post=None,enc=False):
    self.fingerprints = []
    for bary in self.recv():
      self.file,self.pad = bary,0
      if enc:
        self.file,self.pad = self.AESenc(bary,32)
      self.md5 = hashlib.md5(self.file).hexdigest()
      self.p = Path(self.tmpdir,self.md5)
      if pre:pre()
      with self.p.open("wb") as f:
        f.write(self.file)
      if post:post()
      self.fingerprints.append([self.md5,self.pad])
    self.p = Path(self.tmpdir,"index.json")
    if pre:pre()
    with self.p.open("w") as f:
      f.write(json.dumps(self.fingerprints))
    if post:post()

class Download:
  def __init__(self):
    self.tmpdir = "/tmp"

  def AESdec(self,bin,pad):
    bary = bytearray(bin)
    cipher = AES.new(self.key)
    result = bytearray(cipher.decrypt(bin))
    for i in range(0,pad):
      result.pop()
    return result

  def create(self,pre=None,post=None,dec=False):
    self.p = Path(self.tmpdir,"index.json")
    if pre:pre()
    with self.p.open("r") as f:
      self.fingerprints = json.loads(f.read())
    if post:post()
    for line in self.fingerprints:
      fingerprint,pad = line[0],line[1]
      self.p = Path(self.tmpdir,fingerprint)
      if pre:pre()
      with self.p.open("rb") as f:
        bin = f.read()
      self.file = bin
      if dec:
        self.file = self.AESdec(bin,pad)
      if post:post()