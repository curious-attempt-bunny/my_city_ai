import json
import os.path
import sys

from dataclasses import dataclass
from multiprocessing import Pool
from typing import Optional, Any

import fixtures

from rollout import Rollout
from state import State

TABLE = {}

if os.path.isfile('table.json'):
    with open('table.json', 'r') as f:
        for line in f.readlines():
            TABLE.update(json.loads(line))

@dataclass
class Move:
    x: Optional[int]
    y: Optional[int]
    piece_index: Optional[int]
    piece_rotation: Optional[int]

    def is_skip_move(self):
        return self.x is None

class TableActor:
    def __init__(self):
        pass

    def calculate(self, state: State, piece_index: int):
        key = str(piece_index)+"|"+state.key()
        if key not in TABLE:
            candidates = []
            for piece_rotation in range(len(fixtures.PIECE_ROTATIONS[piece_index])):
                piece = fixtures.PIECE_ROTATIONS[piece_index][piece_rotation]
                for y in range(fixtures.HEIGHT):
                    for x in range(fixtures.WIDTH):
                        if state.is_legal_place(piece, x, y):
                            next_state = state.copy()
                            next_state.place(piece, x, y, piece_index)
                            if next_state.score_delta > state.score_delta-1:
                                candidates.append((piece_rotation,x,y))

            if len(candidates) > 0:
                score_delta_total = {}
                depth = 10
                n = 0 

                c = len(candidates)
                t = 0
                passes = 0
                while c > 1:
                    t += c
                    c = int(c/2)
                    passes += 1
                print(''.join('-'*t))

                scale_sum = 0
                scale = 1
                for i in range(passes):
                    scale *= 2
                    scale_sum += scale

                if scale_sum > 0:
                    depth = int(5000/scale_sum) # int(5000/scale)
                else:
                    depth = 10

                while len(candidates) > 1:
                    best_move = None
                    worst_move = None
                    depth *= 2
                    n += depth
                    # print(f'Rollouts {n} -- {len(candidates)} moves remaining')
                    
                    with Pool(7) as p:
                        rollouts = [Rollout(state, candidate, piece_index, depth) for candidate in candidates]
                        representatives = p.map(Rollout.rollout, rollouts)
                    
                    for candidate, representative in zip(candidates, representatives):
                        piece_rotation, x, y = candidate
                        piece = fixtures.PIECE_ROTATIONS[piece_index][piece_rotation]
                        key = f'{piece_rotation}/{x}/{y}'
                        if not key in score_delta_total:
                            score_delta_total[key] = 0
                        score_delta_total[key] += representative.score_delta * depth
                        representative.score_delta = score_delta_total[key] / n

                        if best_move is None or representative.score_delta > best_move[0]:
                            best_move = (representative.score_delta, piece_rotation, x, y)
                            # print("^^^ BEST")
                        if worst_move is None or representative.score_delta < worst_move[0]:
                            worst_move = (representative.score_delta, piece_rotation, x, y)
                            # print("^^^ WORST")

                    candidates = sorted(candidates, key=lambda candidate: -score_delta_total[f'{candidate[0]}/{candidate[1]}/{candidate[2]}'])
                    candidates = candidates[0:int(len(candidates)/2)]

            piece_rotation = None
            x = None
            y = None
            if len(candidates) > 0:
                print()
                piece_rotation, x, y = candidates[0]
            
            key = str(piece_index)+"|"+state.key()
            print({key: (x, y, piece_rotation)})
            with open('table.json', 'a') as f:
                json.dump({key: (x, y, piece_rotation)}, fp=f)
                f.write("\n")
            TABLE[key] = (x, y, piece_rotation)
    
        x, y, piece_rotation = TABLE[key]
        return Move(x, y, piece_index, piece_rotation)
        
