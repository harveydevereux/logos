from typer import Option, Argument, Typer

from typing import Annotated
from pathlib import Path
from datetime import date
import os
from subprocess import call

import builtins

from logos.types.log import Log

app = Typer()


def _date_from_argument(entry: str):
    requested = None
    if entry is not None:
        requested = date.fromisoformat(entry)
        if requested > date.today():
            raise ValueError(f"Date {entry} is in the future.")
    return requested

def _check_path(path: Path | None) -> Path:
    if path is None:
        return Path(os.getenv("LOGOS_ROOT", "./"))
    return path

@app.command()
def tasks(
    root_directory: Annotated[Path | None, Option(help="The root of the log files.")] = None,
    show_complete: Annotated[bool, Option(help="Include complete tasks")] = False,
):
    """
    Report outstanding tasks.
    """
    Log(_check_path(root_directory)).show_tasks(show_complete)


@app.command()
def show(
    entry: Annotated[
        str | None,
        Argument(help="The date of an entry to print, in YYYY-MM-DD format."),
    ] = None,
    root_directory: Annotated[Path | None, Option(help="The root of the log files.")] = None
):
    """
    Show the given, or last, entry.
    """
    root_directory = _check_path(root_directory)
    requested = _date_from_argument(entry)
    if requested is None:
        entry_to_show = Log(root_directory).last()
    else:
        entry_to_show = Log(root_directory).entry_at_date(requested)
        if entry_to_show is None:
            print(f"No entry at date {entry}")
            exit()

    print(f"Dated: {entry_to_show.date}\n")
    with builtins.open(entry_to_show.path, "r") as io:
        for line in io:
            out = line.rstrip("\n")
            print(f"    {out}")


@app.command()
def list(
    root_directory: Annotated[Path | None, Option(help="The root of the log files.")] = None
):
    """List the available entries"""
    Log(_check_path(root_directory)).show_entries()


@app.command()
def open(
    entry: Annotated[
        str | None, Argument(help="The date of an entry to open, in YYYY-MM-DD format.")
    ] = None,
    root_directory: Annotated[Path | None, Option(help="The root of the log files.")] = None
):
    """
    Open the current (or dated) entry.
    """
    root_directory = _check_path(root_directory)
    requested = _date_from_argument(entry)
    if requested is None:
        requested = date.today()

    year, smonth, day = requested.strftime("%Y-%B-%d").split("-")
    year, imonth, day = requested.strftime("%Y-%m-%d").split("-")
    folder = root_directory / year / smonth
    if not folder.exists():
        os.makedirs(folder)

    file = folder / f"{year}-{imonth}-{day}.md"
    EDITOR = os.environ.get("EDITOR") if os.environ.get("EDITOR") else "vim"
    call([EDITOR, file])


@app.command()
def task_path(
    task_hash: Annotated[str, Argument(help="The hash of a task to search for.")],
    root_directory: Annotated[Path | None, Option(help="The root of the log files.")] = None
):
    """
    Return the path to a task form its hash.
    """
    path = Log(_check_path(root_directory)).task_to_path(task_hash)
    if path is not None:
        print(path)
    else:
        print("Task not found.")


@app.command()
def complete(
    task_hash: Annotated[
        str, Argument(help="The hash of a task to mark as completed.")
    ],
    root_directory: Annotated[Path | None, Option(help="The root of the log files.")] = None
):
    """
    Mark a task as complete (and write to the file).
    """
    Log(_check_path(root_directory)).setComplete(task_hash, True)


@app.command()
def uncomplete(
    task_hash: Annotated[
        str, Argument(help="The hash of a task to mark as not completed.")
    ],
    root_directory: Annotated[Path | None, Option(help="The root of the log files.")] = None
):
    """
    Mark a task as incomplete (and write to the file).
    """
    Log(_check_path(root_directory)).setComplete(task_hash, False)
