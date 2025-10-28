from pathlib import Path
from typing import Iterable
from datetime import date

from logos.types.task import Task
from logos.types.entry import Entry

class Log:
    def __init__(self, root: Path):
        self.categories = self._get_dirs(root)
        self.entries = dict()

        for category in self.categories:
            self.entries[category] = []
            for year in self._get_dirs(category):
                for month in self._get_dirs(year):
                    for entry in self._get_files(month):
                        self.entries[category].append(Entry(entry))

        self._task_to_entry = dict()
        for category in self.categories:
            for entry in self.entries[category]:
                for task in entry.tasks.values():
                    self._task_to_entry[task.hash] = entry

        hashes = []
        for category in self.categories:
            for entry in self.entries[category]:
                for task in entry.tasks.values():
                    hashes.append(task.hash)

        m = min(len(h) for h in hashes)
        self._prune_length = m
        for length in range(1, m+1):
            pruned = set(hash[:length] for hash in hashes)
            if len(pruned) == len(hashes):
                self._prune_length = length
                break

        self._prune_length = max(4, self._prune_length)
        self._pruned_to_hash = {hash[:self._prune_length]: hash for hash in hashes}

    def task_to_path(self, hash: str) -> Path:
        hash = self._to_full_hash(hash)

        if hash in self._task_to_entry:
            return self._task_to_entry[hash].path

    def show_tasks(self, show_complete: bool):
        today = date.today()

        for category in self.categories:
            outstanding = 0
            complete = 0
            tasks = dict()
            for entry in self.entries[category]:
                if len(entry.tasks) > 0:
                    tasks[entry.date] = []
                    for _, task in entry.tasks.items():
                        tasks[entry.date].append(task)
                        outstanding += not task.complete
                        complete += task.complete

            print(f"{category}:\n Outstanding tasks: {outstanding}")
            for start_date in tasks:
                days_past = (today-start_date).days
                for task in tasks[start_date]:
                    if not task.complete:
                        print(f"    Age: {days_past} days ({start_date})")
                        print(f"      [0x{task.hash[:self._prune_length]}] {task.name} ")

            if show_complete:
                print(f"\n Complete tasks: {complete}")
                for start_date in tasks:
                    for task in tasks[start_date]:
                        if task.complete:
                            print(f"    Dated: {start_date}")
                            print(f"      [0x{task.hash[:self._prune_length]}] {task.name} ")

    def lastest(self) -> Entry:
        for category in self.categories:
            entry_by_date = {entry.date: entry for entry in self.entries[category]}
            return entry_by_date[list(reversed(sorted(entry_by_date)))[0]]

    def setComplete(self, hash: str, complete: bool) -> None:
        hash = self._to_full_hash(hash)
        self._task_to_entry[hash].setComplete(hash, complete)

    def _get_dirs(self, path: Path) -> Iterable[Path]:
        return [p for p in path.glob('[!.!__]*') if p.is_dir()]

    def _get_files(self, path: Path) -> Iterable[Path]:
        return [p for p in path.glob('[!.]*') if p.is_file()]

    def _to_full_hash(self, hash: str) -> str:
        hash = hash.lstrip("0x").lower()
        if hash in self._pruned_to_hash:
            hash = self._pruned_to_hash[hash]
        return hash