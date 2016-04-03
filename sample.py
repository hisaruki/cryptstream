#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cryptstream

u = cryptstream.Upload()
u.tmpdir = "/home/hisaruki/Desktop"
u.recv()
print(u.fingerprints)

