import random

from fixtures import PIECE_ROTATIONS
from state import State
from actor import TableActor
from fixtures import visualize, PIECES

if __name__ == '__main__':
    # random.seed(1234)
    # random.seed(2345)
    # random.seed(3456)
    # random.seed(4567)
    # random.seed(5678)
    random.seed(6789)
    seeds = [random.randint(0,10000) for i in range(1000)]

    state = State()
    actor = TableActor()

    while not state.is_end():
        random.seed(seeds.pop())
        piece_index = state.random_piece()

        print()
        print('============')
        print(PIECES[piece_index])
        print()
        print(state.visualize())
        print(state.key())

        move = actor.calculate(state, piece_index)

        if move.is_skip_move():
            state.skip_placement(piece_index)
        else:
            piece = PIECE_ROTATIONS[piece_index][move.piece_rotation]
            assert state.is_legal_place(piece, move.x, move.y)
            state.place(piece, move.x, move.y, piece_index)

    print('============')
    print()
    print(state.visualize())
