#!/usr/bin/env python3

import sys
from typing import DefaultDict


def main():
    history = DefaultDict(list)
    with open(sys.argv[1], "r") as f:
        for line in f.readlines():
            try:
                if line.split()[0] == "sudo":
                    cmd = line.split()[1]
                else:
                    cmd = line.split()[0]
                history[cmd].append(line.strip())
            except:
                # print(f"Couldn't split line {line}")
                pass
    for k, v in history.items():
        print(f"# {k}")
        for item in sorted(v):
            print(f"`{item}`\n")


if __name__ == "__main__":
    main()
