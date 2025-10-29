from pathlib import Path
from datetime import date
from hashlib import sha1
from warnings import warn

from logos.types.task import task_from_markdown, is_task


class Entry:
    def __init__(self, file: Path):
        self.path = file
        self._hash = self._file_hash()
        self.date = date.fromisoformat(str(self.path).split("/")[-1].split(".")[0])
        with open(self.path, "r") as io:
            tasks = [task_from_markdown(line) for line in io.readlines()]

        self.tasks = dict()
        for task in tasks:
            if task is not None:
                self.tasks[task.hash] = task

    def setComplete(self, task: str, complete: bool) -> None:
        if task in self.tasks:
            self.tasks[task].complete = complete
            self._write()

    def _write(self) -> None:
        if self._file_hash() != self._hash:
            warn(f"Entry at {self.path} has changed since last read")

        lines = ""
        with open(self.path, "r") as io:
            for line in io.readlines():
                if not is_task(line):
                    lines += line
                else:
                    task = task_from_markdown(line)
                    if task.hash in self.tasks:
                        task = self.tasks[task.hash]
                    else:
                        if self._file_hash() != self._hash:
                            warn(f"Entry at {self.path} has new task:\n  {str(task)}")
                    lines += str(task)

        with open(self.path, "w") as io:
            for line in lines:
                io.write(line)

    def _file_hash(self) -> str:
        sha = sha1()
        with open(self.path, "r") as io:
            for line in io.readlines():
                sha.update(line.encode())
        return sha.hexdigest()
