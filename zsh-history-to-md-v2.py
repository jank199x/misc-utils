#!/usr/bin/env python3

import json
import re
import sys
from collections import defaultdict
from datetime import datetime
from itertools import chain
from operator import itemgetter


def cleaned(command_line: str) -> str:

    line = (
        command_line.decode("utf-8", errors="ignore")
        .strip()
        .split(";")[-1]
        .removeprefix("sudo ")
    )
    return line


def word_is_fine(word: str) -> bool:
    alphanumeric = word.isalnum()
    all_digits = word.isdigit()
    single_symbol = len(word) <= 1
    contains_cyrillic = bool(re.search("[а-яА-Я]", word))

    is_fine = (
        alphanumeric and not all_digits and not single_symbol and not contains_cyrillic
    )

    return is_fine


def get_words(lines: list[str]) -> set[str]:

    raw_words = chain.from_iterable(line.split() for line in lines)
    filtered_words = set(word.lower() for word in raw_words if word_is_fine(word))
    return filtered_words


def grouped(lines: list[str]) -> dict[list]:

    words = get_words(lines)

    groups = defaultdict(list)
    for line in lines:
        for word in words:
            if word in line.split():
                groups[word].append(line)

    return groups


def sorted_dict(values: dict[list]) -> dict[list]:
    return dict(sorted({k: sorted(v) for k, v in values.items()}.items(), key=itemgetter(0)))

def print_to_stdout(groups: dict[list]) -> None:
    today = datetime.now().date().isoformat()
    print(f"# ZSH History {today}\n", file=sys.stdout)
    for k, v in groups.items():
        print(f"## {k}\n", file=sys.stdout)
        for item in sorted(v):
            print(f"`{item}`\n", file=sys.stdout)

def save_to_file(groups: dict[list]) -> None:
    with open("zsh_history_grouped.json", "w", encoding="utf-8") as f:
            json.dump(groups, f, ensure_ascii=False, indent=1)

if __name__ == "__main__":
    # with open(sys.argv[1], "rb") as f:
    with open("/home/jank/.history-zsh", "rb") as f:
        clean_lines = set([cleaned(line) for line in f.readlines()])
    groups = grouped(clean_lines)
    sorted_groups = sorted_dict(groups)
    print_to_stdout(sorted_groups)
