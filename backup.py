#!/usr/bin/env python3

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
