import json
import logging
from datetime import datetime
from typing import Any, Tuple

import requests
from bs4 import BeautifulSoup as bs  # type: ignore

BASEFILENAME = "tarot"
EDGE_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
BASE_URL = "http://www.learntarot.com/"
CARDS = (
    "maj01",
    "maj02",
    "maj03",
    "maj04",
    "maj05",
    "maj06",
    "maj07",
    "maj08",
    "maj09",
    "maj10",
    "maj11",
    "maj12",
    "maj13",
    "maj14",
    "maj15",
    "maj16",
    "maj17",
    "maj18",
    "maj19",
    "maj20",
    "maj21",
    "wa",
    "w2",
    "w3",
    "w4",
    "w5",
    "w6",
    "w7",
    "w8",
    "w9",
    "w10",
    "wpg",
    "wkn",
    "wqn",
    "wkg",
    "ca",
    "c2",
    "c3",
    "c4",
    "c5",
    "c6",
    "c7",
    "c8",
    "c9",
    "c10",
    "cpg",
    "ckn",
    "cqn",
    "ckg",
    "sa",
    "s2",
    "s3",
    "s4",
    "s5",
    "s6",
    "s7",
    "s8",
    "s9",
    "s10",
    "spg",
    "skn",
    "sqn",
    "skg",
    "pa",
    "p2",
    "p3",
    "p4",
    "p5",
    "p6",
    "p7",
    "p8",
    "p9",
    "p10",
    "ppg",
    "pkn",
    "pqn",
    "pkg",
)


def get_card_description_raw(card: str) -> str:
    headers = {"User-Agent": EDGE_USER_AGENT}
    uri = f"{BASE_URL}{card}.htm"
    r = requests.get(uri, headers=headers)
    return r.text


def parse_description(
    text: str,
) -> Tuple[str, list[str], list[dict[str, list[str]]], list[str]]:
    soup = bs(text, "html.parser")
    title = soup.find("h1").text
    keywords = [keyword.text for keyword in soup.find("ul").find_all("li")]
    actions = []
    actions_raw = soup.find("dt").text.split("\r\n\r\n\n")
    if len(actions_raw) < 2:
        actions_raw = soup.find("dt").text.split("\r\n\n")
    for action in actions_raw:
        temp = action.split("\n")
        temp = [a.strip() for a in temp if a.strip()]
        actions.append(
            {
                "term": temp[0],
                "definitions": temp[1:],
            }
        )
    description_raw = (
        soup.find("a", attrs={"name": "description"}).parent.find("p").text.split("\n")
    )
    description = [a.strip() for a in description_raw if a.strip()][:-2]

    return (
        title,
        keywords,
        actions,
        description,
    )


def dump_to_file(cards: dict[str, Any], filename: str = "sample") -> None:

    json_object = json.dumps(cards, indent=4)
    with open(filename + ".json", "w") as outfile:
        outfile.write(json_object)


if __name__ == "__main__":
    timestamp = datetime.now().strftime("%y%m%d-%H%M%S")
    filename = f"{BASEFILENAME}-{timestamp}"
    dump = {}

    test_cards = (
        # "w4",
        # "wkn",
    )

    for i, card in enumerate(test_cards or CARDS):
        logging.warning(f"{i+1}/{len(CARDS)}: Getting {card}")
        desc = get_card_description_raw(card)
        (
            title,
            keywords,
            actions,
            description,
        ) = parse_description(desc)
        dump[card] = {
            "title": title,
            "keywords": keywords,
            "actions": actions,
            "description": description,
        }
        dump_to_file(cards=dump, filename=filename)
