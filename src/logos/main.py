from typer import Option, Argument, Typer

from typing import Annotated
from pathlib import Path

from logos.types.log import Log

app = Typer()

@app.command()
def tasks(
    root_directory: Annotated[
        Path,
        Option(help="The root of the log files.")
    ] = Path("./")
):
    """
    Report outstanding tasks.
    """
    log = Log(root_directory)
    log.show_tasks()

@app.command()
def latest(
    root_directory: Annotated[
        Path,
        Option(help="The root of the log files.")
    ] = Path("./")
):
    """
    Report the latest entry.
    """
    log = Log(root_directory)
    last = log.lastest()
    print(f"Dated: {last.date}\n")
    with open(last.path, "r") as io:
        for line in io:
            print(f"    {line}")

@app.command()
def task_path(
    task_hash: Annotated[
        str,
        Argument(help="The hash of a task to search for.")
    ],
    root_directory: Annotated[
        Path,
        Option(help="The root of the log files.")
    ] = Path("./")
):
    """
    Return the path to a task form its hash.
    """
    log = Log(root_directory)
    path = log.task_to_path(task_hash)
    if path is not None:
        print(path)
    else:
        print("Task not found.")


