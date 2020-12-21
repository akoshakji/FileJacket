#!/usr/bin/env python3

# Documentation on Dropbox - Python API
# https://dropbox-sdk-python.readthedocs.io/en/latest/index.html

import os

from Synchronizer import Synchronizer

# list of directories/files to be uploaded
FILES = ('Desktop',
         'dv',
         'sim',
         '.bash_profile',
         '.mm',
         '.spack',
         '.vimrc')

HOME = os.environ['HOME']
for item in FILES:
    localpath = HOME + '/' + item
    print(localpath)
    sync = Synchronizer(localpath, '/test/')
    sync.synchronize()

print("all done!")
