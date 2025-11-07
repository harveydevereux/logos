from logos.types.entry import Entry

from hashlib import sha1
from datetime import date

ENTRY = r"""
This is some test.

Is an entry.

- [ ] a task
    - [ ] that has
    - [x] some sub
    - [x] tasks

- [x] another task

- [ ] a task with
    - [ ] a sub
        - [ ] sub task
"""

TODAY = date.today()
STODAY = TODAY.strftime("%Y-%m-%d")

TASK_NAMES = [
    "a task",
    "that has",
    "some sub",
    "tasks",
    "another task",
    "a task with",
    "a sub",
    "sub task",
]


def test_entry(tmp_path):
    path = f"{tmp_path}/{STODAY}.md"
    with open(path, "w") as io:
        io.write(ENTRY)

    entry = Entry(path)

    assert entry.date == TODAY
    assert entry.path == path

    assert len(entry.tasks) == 8

    task_names = [task.name for task in entry.tasks.values()]

    assert sorted(set(task_names)) == sorted(set(TASK_NAMES))

    name_to_hash = {name: sha1(name.encode()).hexdigest() for name in task_names}
    for hash in name_to_hash.values():
        assert hash in entry.tasks

    assert entry.task_parent[name_to_hash["a task"]] is None
    assert entry.task_parent[name_to_hash["another task"]] is None
    assert entry.task_parent[name_to_hash["a task with"]] is None

    assert entry.task_parent[name_to_hash["that has"]] == name_to_hash["a task"]
    assert entry.task_parent[name_to_hash["some sub"]] == name_to_hash["a task"]
    assert entry.task_parent[name_to_hash["tasks"]] == name_to_hash["a task"]

    assert entry.task_parent[name_to_hash["a sub"]] == name_to_hash["a task with"]
    assert entry.task_parent[name_to_hash["sub task"]] == name_to_hash["a sub"]
