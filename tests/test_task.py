from logos.types.task import is_task


def test_task_identification(tmp_path):
    not_task = (
        "not a task",
        "- still [] not a task",
        "-[] not a task",
        "-[x] not a task",
        "- [x ] not a task",
        "not a - [ ] task either",
    )
    task = ("- [ ] a valid task", "- [x] also a task")

    for counter_example in not_task:
        assert not is_task(counter_example)

    for example in task:
        assert is_task(example)
