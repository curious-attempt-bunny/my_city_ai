import fixtures
import random

class State:
    def __init__(self, cells = None, legal_moves = None, pieces_remaining = None, turn_number = None, score_delta = None):
        if cells is None:
            self.cells = [row.copy() for row in fixtures.CELLS]
            self.legal_moves = [row.copy() for row in fixtures.LEGAL_FIRST_PLAY]
            self.pieces_remaining = [3] * len(fixtures.PIECE_ROTATIONS)
            self.turn_number = 1
            self.score_delta = 0 
        else:
            self.cells = [row.copy() for row in cells]
            self.legal_moves = [row.copy() for row in legal_moves]
            self.pieces_remaining = [v for v in pieces_remaining]
            self.turn_number = turn_number
            self.score_delta = score_delta

    def key(self):
        result = []
        for count in self.pieces_remaining:
            result.append(str(count))
        result.append('|')
        for row in self.cells:
            for cell in row:
                if cell == '#':
                    result.append('1')
                else:
                    result.append('0')
        return ''.join(result)

    def visualize(self):
        return f"Turn {self.turn_number}:\n"+fixtures.visualize(self.cells)+"\n"+str(self.pieces_remaining)+f"\nscore delta: {self.score_delta}"

    def is_end(self):
        return sum(self.pieces_remaining) == 0

    def random_piece(self):
        choices = []
        for piece in range(len(self.pieces_remaining)):
            for _ in range(self.pieces_remaining[piece]):
                choices.append(piece)

        index = random.randint(0, len(choices)-1)

        return choices[index]

    def copy(self):
        state = State(self.cells, self.legal_moves, self.pieces_remaining, self.turn_number, self.score_delta)
        return state

    def is_legal_place(self, piece, x, y):
        is_legal = False
        placed_on = set()

        for yd in range(len(piece)):
            for xd in range(len(piece[0])):
                x2 = xd + x
                y2 = yd + y
                if not fixtures.on_board(x2, y2):
                    return False

                if piece[yd][xd] == '#':
                    if self.cells[y2][x2] in '#X':
                        return False
                    if self.cells[y2][x2] == '-' and '.' in placed_on:
                        return False
                    if self.cells[y2][x2] == '.' and '-' in placed_on:
                        return False
                    placed_on.add(self.cells[y2][x2])

                    if self.legal_moves[y2][x2] == 1:
                        is_legal = True

        return is_legal

    def place(self, piece, x, y, piece_index):
        state = self
        if self.turn_number == 1:
            state.legal_moves = [[0 for x in range(fixtures.WIDTH)] for y in range(fixtures.HEIGHT)]
        state.turn_number = state.turn_number + 1
        
        for yd in range(len(piece)):
            for xd in range(len(piece[0])):
                x2 = xd + x
                y2 = yd + y
                if piece[yd][xd] == '#':
                    assert state.cells[y2][x2] in '-.tr'
                    if state.cells[y2][x2] == 't':
                        state.score_delta -= 2
                    elif state.cells[y2][x2] == 'r':
                        state.score_delta += 2
                    else:
                        state.score_delta += 1
                    state.cells[y2][x2] = '#'

                    for vector in [(1,0), (0,-1), (-1, 0), (0,1)]:
                        x3 = x2 + vector[0]
                        y3 = y2 + vector[1]
                        if fixtures.on_board(x3, y3):
                            state.legal_moves[y3][x3] = 1

        state.pieces_remaining[piece_index] -= 1

        return state

    def skip_placement(self, piece_index):
        state = self
        state.score_delta -= 1
        state.pieces_remaining[piece_index] -= 1

        state.turn_number = state.turn_number + 1
        if self.turn_number == 1:
            state.legal_moves = [[0 for x in range(fixtures.WIDTH)] for y in range(fixtures.HEIGHT)]

        return state

    def rollout(self, piece, x, y, piece_index, n):
        representative = self.copy()
        representative = representative.place(piece, x, y, piece_index)
        total = 0
        for i in range(n):
            state = representative.copy()
            while not state.is_end():
                next = state.random_piece()
                legal = []
                for piece in fixtures.PIECE_ROTATIONS[next]:
                    for y in range(fixtures.HEIGHT):
                        for x in range(fixtures.WIDTH):
                            if state.is_legal_place(piece, x, y):
                                legal.append((piece, x, y))
                
                if len(legal) == 0:
                    state = state.skip_placement(next)
                else:
                    piece, x, y = legal[random.randint(0, len(legal)-1)]
                    state = state.place(piece, x, y, next)

            total += state.score_delta

        representative.score_delta = total / n

        return representative
