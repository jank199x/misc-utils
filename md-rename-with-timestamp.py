#! /usr/bin/env python3

import os
import re
import subprocess
from datetime import datetime
from glob import glob


def _addtimestamp(filename: str) -> str:
    stat_result = subprocess.run(["stat", "-c", "%W", filename], capture_output=True)
    created_epoch = int(stat_result.stdout)

    updated_epoch = os.path.getmtime(filename)

    timestamp_epoch = updated_epoch if updated_epoch < created_epoch else created_epoch

    timestamp_datetime = datetime.fromtimestamp(timestamp_epoch)
    formatted_datetime = timestamp_datetime.strftime("%y%m%d-%H%M%S")

    timestamped = re.match("[\d]{6}\-[\d]{6}.*\.md", filename)
    if timestamped:
        filename = filename[14:]

    formatted_filename = re.sub(r"[^a-zA-Z0-9\s\-]", "", filename)
    formatted_filename = formatted_filename[:-2]
    formatted_filename = "-".join(formatted_filename.split()[:5])
    formatted_filename = formatted_filename.lower()

    new_name = f"{formatted_datetime}-{formatted_filename}.md"

    return new_name


def addtimestamp() -> None:
    quit = False

    markdown_notes = glob("*.md")
    total = len(markdown_notes)

    for i, note in enumerate(markdown_notes):
        while True:
            new_name = _addtimestamp(note)
            yaynay = input(f"{i+1}/{total}: Rename {note} -> {new_name}? [Y]/n/q\n")
            if yaynay in "Yy" or yaynay == "":
                os.rename(note, new_name)
                break
            elif yaynay in "Nn":
                break
            elif yaynay in "Qq":
                quit = True
                break
            else:
                print("Y/N/Q only!")
        if quit:
            break


if __name__ == "__main__":
    addtimestamp()
