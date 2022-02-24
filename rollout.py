import sys

from dataclasses import dataclass
from typing import Any

import fixtures

from state import State

@dataclass
class Rollout:
    state: State
    candidate: Any
    piece_index: int
    depth: int

    def rollout(self):
        piece_rotation, x, y = self.candidate
        piece = fixtures.PIECE_ROTATIONS[self.piece_index][piece_rotation]
        result = self.state.rollout(piece, x, y, self.piece_index, self.depth)
        print('.', end='')
        sys.stdout.flush()
        return result