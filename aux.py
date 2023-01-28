import numpy as np

def get_neighbors(index, clockwise):
    neighbors = []
    if clockwise:
        neighbors.append((index - 1) % 8)
        neighbors.append((index + 1) % 8)
    else:
        neighbors.append((index + 1) % 8)
        neighbors.append((index - 1) % 8)
    return neighbors


def is_corner(dir):
    switch = {
        0: True,
        1: False,
        2: True,
        3: False,
        4: True,
        5: False,
        6: True,
        7: False
    }
    return switch.get(dir, False)


def valid_position(row, col, shape):
    height, width, aux = shape
    if row == -1:
        row = height - 1
    elif row == height:
        row = 0

    if col == -1:
        col = width - 1
    elif col == width:
        col = 0
    
    return row, col


def get_animals_around(grid, row, col, animal):
    if animal == "rabbit":
        animal_index = 0
    elif animal == "fox":
        animal_index = 1

    height, width = grid.shape[:2]
    if valid_position(row, col, grid.shape) != (row, col):
        print("Invalid position: ({}, {})".format(row, col))
        return None
    map = np.zeros(8, dtype=int)
    
    for i in range(3):
        valid_row, valid_col = valid_position(row - 1, col - 1 + i, grid.shape)
        map[i] = grid[valid_row, valid_col, animal_index] 
    valid_row, valid_col = valid_position(row, col + 1, grid.shape)
    map[3] = grid[valid_row, valid_col, animal_index]    

    for i in range(3):
        valid_row, valid_col = valid_position(row + 1, col + 1 - i, grid.shape)
        map[4 + i] = grid[valid_row, valid_col, animal_index]    
    valid_row, valid_col = valid_position(row, col - 1, grid.shape)
    map[7] = grid[valid_row, valid_col, animal_index]
    return map


