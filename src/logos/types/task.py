from hashlib import sha1
from re import search

class Task:
    def __init__(self, name: str, complete: bool):
        self._name = name.replace('\n','').strip()
        self.complete = complete
        self._hash = sha1(self.name.encode()).hexdigest()

    @property
    def name(self) -> str: return self._name

    @property
    def hash(self) -> str: return self._hash

    def __str__(self) -> str:
        return f"- [{'x' if self.complete else ' '}] {self.name}"


def is_task(line: str) -> bool:
    return search("^(\s*)- \[( |x)\] (.+)$", line) is not None

def task_from_markdown(line: str) -> Task | None:
    if is_task(line):
        name = line.split(']')[-1]
        complete = True if search("^(\s*)- \[x\] (.+)$", line) else False
        return Task(name, complete)