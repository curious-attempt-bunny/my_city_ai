BOARD = """
--t--.....r
r----...t.X
X---......X
X---..t...r
XX-......XX
Xr---...rXX
X----...XXX
----..t.rXX
r--.....XXX
--....rXXXX
"""

def visualize(matrix):
    return "\n".join([
        ''.join(map(str, row))
        for row in matrix
    ])

def cellify(repr):
    return list(map(list, repr.split("\n")[1:-1]))

CELLS = cellify(BOARD)
WIDTH = len(CELLS[0])
HEIGHT = len(CELLS)

# print(visualize(CELLS))

def on_board(x, y):
    return x >= 0 and x < WIDTH and y >= 0 and y < HEIGHT

def opposite(x1, y1, x2, y2):
    if not on_board(x1, y1) or not on_board(x2, y2):
        return False

    if CELLS[y1][x1] == '.' and CELLS[y2][x2] == '-':
        return True
    if CELLS[y1][x1] == '-' and CELLS[y2][x2] == '.':
        return True
    
    return False
    

LEGAL_FIRST_PLAY = [
    [
        1 if opposite(x, y, x-1, y) or opposite(x, y, x+1, y) or opposite(x, y, x, y-1) or opposite(x, y, x, y+1) else 0
        for x in range(WIDTH)
    ]
    
    for y in range(HEIGHT)
]

# print(visualize(LEGAL_FIRST_PLAY))

PIECES = [
"""
####
""",

"""
##
##
""",

"""
 # 
###
""",

"""
 ##
## 
""",

"""
##
""",

"""
###
# #
""",

"""
#  
###
"""
]

def all_rotations(piece):
    # print('all_rotations of')
    # print(visualize(piece))
    rotation_visualizations = set()
    piece_rotations = []
    for x_vector, y_vector in [
        ((1,0), (0,1)),
        ((0,-1), (1,0)),
        ((-1, 0), (0, -1)),
        ((0,1), (-1, 0))
    ]:
        original_width = len(piece[0])
        original_height = len(piece)
        rotated_width = original_width if x_vector[0] != 0 else original_height
        rotated_height = original_height if x_vector[0] != 0 else original_width
        vector = (x_vector[0] + y_vector[0], x_vector[1] + y_vector[1])
        offset_x = 0
        offset_y = 0
        if vector == (1,-1):
            offset_y = original_width-1
        if vector == (-1,-1):
            offset_x = original_width-1
            offset_y = original_height-1
        if vector == (-1, 1):
            offset_x = original_height-1
        
        original_width - 1 if x_vector[0] == -1 else 0
        rotated_piece = [[' ' for x in range(rotated_width)] for y in range(rotated_height)]
        # print('rotation', x_vector, y_vector, vector, offset_x, offset_y, '(', original_height, original_width,')')
        for y in range(original_height):
            for x in range(original_width):
                y2 = x*x_vector[1] + y*y_vector[1] + offset_y
                x2 = x*x_vector[0] + y*y_vector[0] + offset_x
                rotated_piece[y2][x2] = piece[y][x]
                # print(x,y,'-->',x2,y2,piece[y][x])

        viz = visualize(rotated_piece)
        if viz not in rotation_visualizations:
            piece_rotations.append(rotated_piece)
            rotation_visualizations.add(viz)
            # print(viz)
        # else:
        #     print('skipped:')
        #     print(viz)

    return piece_rotations

PIECE_ROTATIONS = [
    all_rotations(cellify(piece))
    for piece in PIECES
]

# for piece_rotations in PIECE_ROTATIONS:
#     for rotation in piece_rotations:
#         print(visualize(rotation))
#         print()