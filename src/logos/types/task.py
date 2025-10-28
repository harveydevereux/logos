from hashlib import sha1
from re import search

class Task:
    def __init__(self, name: str, complete: bool):
        self._name = name.replace('\n','').strip()
        self._complete = complete
        self._hash = sha1(self.name.encode()).hexdigest()

    @property
    def name(self) -> str: return self._name

    @property
    def complete(self) -> bool: return self._complete

    @property
    def hash(self) -> str: return self._hash

def task_from_markdown(line: str) -> Task | None:
    if search("^(\s*)- \[( |x)\] (.+)$", line):
        name = line.split(']')[-1]
        complete = True if search("^(\s*)- \[x\] (.+)$", line) else False
        return Task(name, complete)