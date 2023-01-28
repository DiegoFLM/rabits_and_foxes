import numpy as np

import aux
import strategy as Strategy


class Animal:
    def __init__(self, _row, _col, _species, _strategy, 
        _preferred_direction = None, _clockwise = True,
        _diagonal_prediction = False):

        if _species == "rabbit" or _species == "fox":
            self.species = _species
        else:
            raise ValueError("invalid animal species")

        self.row = _row
        self.col = _col
        self.strategy = _strategy
        self.preferred_direction = _preferred_direction
        self.clockwise = _clockwise
        self.diagonal_prediction = _diagonal_prediction

        if _species == "rabbit":
            self.animal_index = 0
        elif _species == "fox":
            self.animal_index = 1
            self.moves_without_eating = 0


    def get_position(self):
        return (self.row, self.col)


    def get_strategy(self):
        return self.strategy


    def get_moves_without_eating(self):
        return self.moves_without_eating


    def move(self, shape, rabbits_around = None, foxes_around = None):
        if self.species == "fox":
            self.moves_without_eating += 1

        if self.strategy == "random":
            dir =  np.random.randint(0, 8)

        elif self.strategy == "clockwise_escape":
            dir = Strategy.clockwise_escape(foxes_around,
                self.preferred_direction, self.clockwise)

        elif self.strategy == "chasing_1":
            dir = Strategy.chasing_1(rabbits_around, self.preferred_direction,
                self.clockwise, self.diagonal_prediction)
        else:
            raise ValueError("invalid strategy")

        # 0 1 2
        # 7   3
        # 6 5 4

        if (dir < 0) or (dir > 7):
            raise ValueError("Animal.move(): invalid direction")

        if dir == 0:
            self.row -= 1
            self.col -= 1
        elif dir == 1:
            self.row -= 1
        elif dir == 2:
            self.row -= 1
            self.col += 1
        elif dir == 3:
            self.col += 1
        elif dir == 4:
            self.row += 1
            self.col += 1
        elif dir == 5:
            self.row += 1
        elif dir == 6:
            self.row += 1
            self.col -= 1
        elif dir == 7:
            self.col -= 1 

        self.row, self.col = aux.valid_position(self.row, self.col, shape)


    def reproduce(self):
        self.moves_without_eating = 0
        return Animal(self.row, self.col, self.species, self.strategy,
            self.preferred_direction, self.clockwise, self.diagonal_prediction)