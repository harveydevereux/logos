from logos.types.task import is_task, Task, task_from_markdown


def test_task_identification():
    not_task = (
        "not a task",
        "- still [] not a task",
        "-[] not a task",
        "-[x] not a task",
        "- [x ] not a task",
        "not a - [ ] task either",
    )
    task = (
        "- [ ] a valid task",
        "- [x] also a task",
        "- [ ] is a [task]",
        "- [x] is a task a [well]",
    )

    for counter_example in not_task:
        assert not is_task(counter_example)

    for example in task:
        assert is_task(example)


def test_task_name():
    names = ("a valid task", "also a task", "is a [task]", "is a task a [well]")

    for name in names:
        assert Task(name, True).name == name


def test_task_md_conversion():
    names = ("a valid task", "also a task", "is a [task]", "is a task a [well]")

    for name in names:
        assert task_from_markdown("- [ ] " + name).name == name

    for name in names:
        assert task_from_markdown("- [x] " + name).name == name
