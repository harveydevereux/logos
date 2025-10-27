from typer import Option, Typer

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

