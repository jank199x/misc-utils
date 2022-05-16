#! /usr/bin/env python3

import os
import re
from datetime import datetime
from glob import glob


def _addtimestamp(filename: str) -> str:
    created_epoch = os.path.getctime(filename)
    created_datetime = datetime.fromtimestamp(created_epoch)
    formatted_datetime = created_datetime.strftime("%y%m%d-%H%M%S")

    formatted_filename = re.sub(r"[^a-zA-Z0-9\s]", "", filename)
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
            yaynay = input(f"{i+1}/{total}: Rename {note}? Y/N/Q\n")
            if yaynay in "Yy":
                new_name = _addtimestamp(note)
                print(f"{note} -> {new_name}")
                # os.rename(note, new_name)
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
