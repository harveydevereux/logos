from pathlib import Path
from datetime import date
from hashlib import sha1
from warnings import warn

from logos.types.task import task_from_markdown, is_task
from logos.utils import indent_length


class Entry:
    def __init__(self, file: Path):
        self.path = file
        self._hash = self._file_hash()
        self.date = date.fromisoformat(str(self.path).split("/")[-1].split(".")[0])

        self._parse_tasks()

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
                if not is_task(line.lstrip()):
                    lines += line
                else:
                    task = task_from_markdown(line.lstrip())
                    if task.hash in self.tasks:
                        task = self.tasks[task.hash]
                    else:
                        if self._file_hash() != self._hash:
                            warn(f"Entry at {self.path} has new task:\n  {str(task)}")
                    lines += " " * indent_length(line) + str(task) + "\n"

        with open(self.path, "w") as io:
            for line in lines:
                io.write(line)

    def _file_hash(self) -> str:
        sha = sha1()
        with open(self.path, "r") as io:
            for line in io.readlines():
                sha.update(line.encode())
        return sha.hexdigest()

    def _parse_tasks(self) -> None:
        lines = ""
        with open(self.path, "r") as io:
            lines = [line for line in io.readlines() if is_task(line.lstrip())]

        parents = []
        indent = 0
        self.tasks = [task_from_markdown(line.lstrip()) for line in lines]
        self.task_parent = dict()

        for i, line in enumerate(lines):
            line_level = indent_length(line) // 4
            if line_level == 0:
                parents = [None]
                indent = 0
            elif line_level == indent + 1:
                # New indent
                parents.append(i - 1)
                indent += 1
            elif line_level < indent:
                while indent > line_level:
                    parents.pop(-1)
                    indent -= 1

            phash = self.tasks[parents[-1]].hash if parents[-1] is not None else None
            self.task_parent[self.tasks[i].hash] = phash

        self.tasks = {task.hash: task for task in self.tasks}
