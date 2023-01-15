import json
import logging
import time
from datetime import datetime

import certifi
import urllib3
from bs4 import BeautifulSoup as bs

BASE_URL = "https://www.goodreads.com/review/list/11116469-sebastian-gebski"

BASEFILENAME = "gebski"

START_PAGE = 1

DATEFORMATS = ("%b %d, %Y", "%b %Y", "%Y")
UNKNOWNDATES = ("unknown", "not set")

QUERY_PARAMS = {
    "order": "d",
    "print": "true",
    "sort": "read",
    "view": "reviews",
    "shelf": "read",
}

RATING_MAP = {
    "did not like it": "1/5",
    "it was ok": "2/5",
    "liked it": "3/5",
    "really liked it": "4/5",
    "it was amazing": "5/5",
}

SLEEP_TIME = 0.1


def parse_date(date: str) -> str:

    if date.strip() in UNKNOWNDATES:
        return date.strip()

    date = date.replace("not set", "").strip()

    for fmt in DATEFORMATS:
        try:
            return datetime.strptime(date, fmt).date().isoformat()
        except ValueError:
            pass

    logging.warning(f"Could not parse date {date}!")
    return date


def pager(params: dict, page: int) -> dict:
    return {
        **params,
        "page": str(page),
    }


def get_reviews(manager, page=1):

    req = manager.request(
        "GET",
        BASE_URL,
        fields=pager(
            params=QUERY_PARAMS,
            page=page,
        ),
    )

    review_page = bs(req.data.decode("utf-8"), "html.parser")
    return review_page.find_all("tr", class_="bookalike review")


def get_review_id(review) -> str:
    return review["id"].replace("review_", "")


def parse_review(review) -> dict:
    review_json = {}

    review_json["title"] = (
        review.find("td", class_="field title").find("a").text.strip()
    )
    review_json["title"] = " ".join(review_json["title"].split())
    review_json["author"] = (
        review.find("td", class_="field author").find("a").text.strip()
    )
    review_json["isbn"] = (
        review.find("td", class_="field isbn").find("div", class_="value").text.strip()
    )
    review_json["isbn13"] = (
        review.find("td", class_="field isbn13")
        .find("div", class_="value")
        .text.strip()
    )
    review_json["asin"] = (
        review.find("td", class_="field asin").find("div", class_="value").text.strip()
    )
    review_json["date_pub"] = parse_date(
        review.find("td", class_="field date_pub")
        .find("div", class_="value")
        .text.strip()
    )
    review_json["date_pub_edition"] = parse_date(
        review.find("td", class_="field date_pub_edition")
        .find("div", class_="value")
        .text.strip()
    )
    review_json["rating"] = RATING_MAP.get(
        review.find("td", class_="field rating")
        .find("div", class_="value")
        .find("span", class_="staticStars notranslate")
        .get("title")
    )
    review_json["date_added"] = parse_date(
        review.find("td", class_="field date_added")
        .find("div", class_="value")
        .text.strip()
    )
    review_json["date_started"] = parse_date(
        review.find("td", class_="field date_started")
        .find("div", class_="value")
        .text.strip()
    )
    review_json["date_read"] = parse_date(
        review.find("td", class_="field date_read")
        .find("div", class_="value")
        .text.strip()
    )

    review_id = get_review_id(review)
    review_raw = review.find("td", class_="field review").find(
        "span", id=f"freeTextreview{review_id}"
    )
    if review_raw:
        review_json["review"] = [
            str(line) for line in review_raw if str(line) != "<br/>"
        ]
    else:
        review_json["review"] = ""

    return review_json


def dump_to_file(reviews: list, filename: str = "sample") -> None:

    json_object = json.dumps(reviews, indent=4, ensure_ascii=False)
    with open(filename + ".json", "w") as outfile:
        outfile.write(json_object)


def get_gebski_reviews():

    timestamp = datetime.now().strftime("%y%m%d-%H%M%S")
    filename = f"{BASEFILENAME}-{timestamp}"

    logging.basicConfig(
        filename=f"{filename}.log",
        encoding="utf-8",
        level=logging.INFO,
        format="%(asctime)s %(message)s",
    )

    logging.info(f"Downloading Sebastian Gebski's book reviews!")

    manager = urllib3.PoolManager(ca_certs=certifi.where())

    page = START_PAGE
    reviews = []

    while True:
        logging.info(f"Trying to get page {page}")
        bs_reviews = get_reviews(manager, page=page)

        if len(bs_reviews) == 0:
            logging.info(f"Page {page} not found")
            logging.info(f"Finished, got {len(reviews)} reviews")
            break

        logging.info(f"Success! Got {len(bs_reviews)} reviews")
        for review in bs_reviews:
            reviews.append(parse_review(review))

        logging.info(f"Dumping reviews to {filename}.json")
        dump_to_file(reviews=reviews, filename=filename)

        logging.info(f"Sleeping for {SLEEP_TIME} seconds")
        time.sleep(SLEEP_TIME)
        page += 1

    logging.info(f"Dumping reviews to {filename}.json")
    dump_to_file(reviews=reviews, filename=filename)

    return filename


def convert_to_csv(filename):
    import pandas as pd

    with open(f"{filename}.json", encoding="utf-8") as inputfile:
        df = pd.read_json(inputfile)

    df.to_csv(f"{filename}.csv", encoding="utf-8", index=False)


if __name__ == "__main__":
    filename = get_gebski_reviews()
    # convert_to_csv(filename=filename)
