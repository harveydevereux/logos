from pathlib import Path
from datetime import date

from logos.types.task import Task, task_from_markdown

class Entry:
    def __init__(self, file: Path):
        self.path = file
        self.date = date.fromisoformat(str(self.path).split('/')[-1].split('.')[0])
        with open(self.path, "r") as io:
            tasks = [task_from_markdown(line) for line in io.readlines()]

        self.tasks = dict()
        for task in tasks:
            if task is not None:
                self.tasks[task.hash] = task