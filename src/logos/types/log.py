from pathlib import Path
from typing import Iterable
from datetime import date

from logos.types.task import Task, task_from_markdown

class Log:
    def __init__(self, root: Path):
        self.categories = self._get_dirs(root)
        self.entries = dict()

        for category in self.categories:
            self.entries[category] = []
            for year in self._get_dirs(category):
                for month in self._get_dirs(year):
                    for entry in self._get_files(month):
                        self.entries[category].append(entry)

    def show_tasks(self):
        today = date.today()

        for category in self.categories:
            outstanding = 0
            tasks = dict()
            for entry in self.entries[category]:
                entry_date = date.fromisoformat(str(entry).split('/')[-1].split('.')[0])
                entry_tasks = self._extract_tasks(entry)
                if len(entry_tasks) > 0:
                    tasks[entry_date] = []
                    for task in self._extract_tasks(entry):
                        tasks[entry_date].append(task)
                        outstanding += not task.complete

            print(f"{category}:\n Outstanding tasks: {outstanding}")
            for start_date in tasks:
                days_past = (today-start_date).days
                for task in tasks[start_date]:
                    if not task.complete:
                        print(f"    Age: {days_past} days ({start_date})")
                        print(f"      - [ ] {task.name}")

    def _get_dirs(self, path: Path) -> Iterable[Path]:
        return [p for p in path.glob('[!.!__]*') if p.is_dir()]

    def _get_files(self, path: Path) -> Iterable[Path]:
        return [p for p in path.glob('[!.]*') if p.is_file()]

    def _extract_tasks(self, file: Path) -> Iterable[Task]:
        with open(file, "r") as io:
            tasks = [task_from_markdown(line) for line in io.readlines()]

        return [task for task in tasks if task]