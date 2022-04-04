#!/usr/bin/env python3

import os
rootdir = '/home/pavle/Important/smolness/digital-trash'

for subdir, dirs, files in os.walk(rootdir):
    if len(files) == 1:
        print(f'\n{subdir}: {len(files)}')
        file = files[0]
        filepath = os.path.join(subdir, file)
        print(f"{filepath=}")
        subdirname = os.path.basename(subdir)
        _, ext = os.path.splitext(file)
        print(f"{subdirname=} {ext=}")
        parentdir= os.path.dirname(subdir)
        print(f"{parentdir=}")
        renameto = os.path.join(parentdir, subdirname+ext)
        print(f"{renameto=}")
        os.rename(filepath, renameto)

for subdir, dirs, files in os.walk(rootdir):
    if len(files) == 0:
        os.removedirs(subdir)
