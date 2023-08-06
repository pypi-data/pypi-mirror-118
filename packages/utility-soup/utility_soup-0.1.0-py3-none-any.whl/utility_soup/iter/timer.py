import time
from typing import Iterable, TypeVar, List

T = TypeVar('T')


class ForLoopTimer:

    def __init__(self):
        self.loops: List[float] = []
        self.iterable: Iterable[T]

        self._complete = False

    def __call__(self, iterable: Iterable[T]):
        self.iterable = iterable
        return self

    def __iter__(self):
        self.loops.append(time.time())
        iterator = self.iterable.__iter__()
        while True:
            try:
                yield next(iterator)
                self.loops.append(time.time())
            except StopIteration:
                self._create_summary()
                self._complete = True
                return

    def _create_summary(self):
        self.laps = [second - first for first, second in zip(self.loops, self.loops[1:])]
        self.average_lap = sum(self.laps) / len(self.laps)

    def __str__(self):
        return f"""Loops took: {self.laps}"""
