#! /usr/bin/env python

import subprocess
import glob
import click
from enum import Enum


class Actions(Enum):
    UNPACK = "unpack"
    REPACK = "repack"


ClickActions = click.Choice(
    [
        Actions.UNPACK.value,
        Actions.REPACK.value,
    ],
    case_sensitive=False,
)


def unpack():
    processes = []

    cbr = glob.glob("*.cbr")

    for book in cbr:
        process = subprocess.Popen(
            f"unrar -o- x {book} {book[:-4]}/",
            shell=True,
            stdout=subprocess.DEVNULL,
        )
        processes.append(process)

    cbz = glob.glob("*.cbz")

    for book in cbz:
        process = subprocess.Popen(
            f"unzip -n {book} -d {book[:-4]}/",
            shell=True,
            stdout=subprocess.DEVNULL,
        )
        processes.append(process)

    return processes


def repack():
    processes = []
    dirs = glob.glob("./*/")
    dirs = [dir[2:-1] for dir in dirs]
    for dir in dirs:
        process = subprocess.Popen(
            f"zip -r -9 -j {dir}.cbz {dir}",
            shell=True,
            stdout=subprocess.DEVNULL,
        )
        processes.append(process)

    return processes


action_map = {
    Actions.UNPACK.value: unpack,
    Actions.REPACK.value: repack,
}


@click.command()
@click.option("--action", type=ClickActions, required=True)
def main(action):

    processes = action_map[action]()

    for p in processes:
        print(f"{p.pid}: {p.args}: {'ok' if p.wait() == 0 else 'fail'}")


if __name__ == "__main__":
    main()
