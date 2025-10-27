from dataclasses import dataclass

from re import search

@dataclass
class Task:
    def __init__(self, name: str, complete: bool):
        self.name = name.replace('\n','').strip()
        self.complete = complete

def task_from_markdown(line: str) -> Task | None:
    if search("^(\s*)- \[( |x)\] (.+)$", line):
        name = line.split(']')[-1]
        complete = True if search("^(\s*)- \[x\] (.+)$", line) else False
        return Task(name, complete)