from logos.types.entry import Entry

from datetime import date

ENTRY = r"""
This is some test.

In an entry.

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


def test_entry(tmp_path):
    path = f"{tmp_path}/{STODAY}.md"
    with open(path, "w") as io:
        io.write(ENTRY)

    entry = Entry(path)

    assert entry.date == TODAY
    assert entry.path == path

    assert len(entry.tasks) == 8

    task_names = [task.name for task in entry.tasks.values()]

    assert "a task" in task_names
    assert "that has" in task_names
    assert "some sub" in task_names
    assert "tasks" in task_names
    assert "another task" in task_names
    assert "a task with" in task_names
    assert "a sub" in task_names
    assert "sub task" in task_names
