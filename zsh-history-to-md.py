#!/usr/bin/env python3

from datetime import datetime
import sys
from typing import DefaultDict


def main():
    history = DefaultDict(list)
    with open(sys.argv[1], "rb") as f:
        for line in f.readlines():
            line = line.decode('utf-8',errors='ignore')
            line = line.split(";")[-1]
            try:
                if line.split()[0] == "sudo":
                    cmd = line.split()[1]
                else:
                    cmd = line.split()[0]
                if line.strip() not in history[cmd]:
                    history[cmd].append(line.strip())
            except:
                # print(f"Couldn't split line {line}")
                pass
    today = datetime.now().date().isoformat()
    print(f"# ZSH History {today}\n", file=sys.stdout)
    for k, v in history.items():
        print(f"## {k}\n", file=sys.stdout)
        for item in sorted(v):
            print(f"`{item}`\n", file=sys.stdout)


if __name__ == "__main__":
    main()
