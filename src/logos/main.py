from typer import Option, Argument, Typer

from typing import Annotated
from pathlib import Path

from logos.types.log import Log

app = Typer()


@app.command()
def tasks(
    root_directory: Annotated[Path, Option(help="The root of the log files.")] = Path(
        "./"
    ),
    show_complete: Annotated[bool, Option(help="Include complete tasks")] = False,
):
    """
    Report outstanding tasks.
    """
    Log(root_directory).show_tasks(show_complete)


@app.command()
def latest(
    root_directory: Annotated[Path, Option(help="The root of the log files.")] = Path(
        "./"
    ),
):
    """
    Report the latest entry.
    """
    log = Log(root_directory)
    last = log.lastest()
    print(f"Dated: {last.date}\n")
    with open(last.path, "r") as io:
        for line in io:
            out = line.rstrip("\n")
            print(f"    {out}")


@app.command()
def task_path(
    task_hash: Annotated[str, Argument(help="The hash of a task to search for.")],
    root_directory: Annotated[Path, Option(help="The root of the log files.")] = Path(
        "./"
    ),
):
    """
    Return the path to a task form its hash.
    """
    path = Log(root_directory).task_to_path(task_hash)
    if path is not None:
        print(path)
    else:
        print("Task not found.")


@app.command()
def complete(
    task_hash: Annotated[
        str, Argument(help="The hash of a task to mark as completed.")
    ],
    root_directory: Annotated[Path, Option(help="The root of the log files.")] = Path(
        "./"
    ),
):
    """
    Mark a task as complete (and write to the file).
    """
    Log(root_directory).setComplete(task_hash, True)


@app.command()
def uncomplete(
    task_hash: Annotated[
        str, Argument(help="The hash of a task to mark as not completed.")
    ],
    root_directory: Annotated[Path, Option(help="The root of the log files.")] = Path(
        "./"
    ),
):
    """
    Mark a task as incomplete (and write to the file).
    """
    Log(root_directory).setComplete(task_hash, False)
