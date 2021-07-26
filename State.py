from __future__ import annotations
from typing import Iterable


class Move:
    pass


class State:
    def available_moves(self) -> Iterable[Move]:
        raise NotImplementedError()

    def is_finished(self) -> bool:
        raise NotImplementedError()

    def move(self, move: Move) -> State:
        raise NotImplementedError()