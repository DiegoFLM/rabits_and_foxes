import numpy as np

import aux


class Strategy:

    # This method receives an array
    # of length 8, the amount of foxes around 
    # and returns the next state.
    # The current state (f) is an array of eight integers, 
    # f[i] := amount of foxes in the i-th direction
    # state index, same as directions:
    # 0 1 2
    # 7   3
    # 6 5 4
    @staticmethod
    def clockwise_escape(f, preferred_direction, clockwise):
        neighbors = aux.get_neighbors(preferred_direction, clockwise)
        if not ( f[preferred_direction] 
                or f[neighbors[0]] 
                or f[neighbors[1]] ):
            return preferred_direction # safe from visible foxes

        current_direction = preferred_direction
        evaluated_safer_directions = 1
        while evaluated_safer_directions < 8:
            if clockwise:
                current_direction = (current_direction + 1) % 8
            else:
                current_direction = (current_direction - 1) % 8

            neighbors = aux.get_neighbors(current_direction, clockwise)
            if not ( f[current_direction] 
                    or f[neighbors[0]] 
                    or f[neighbors[1]] ):
                return current_direction # safe from visible foxes
            evaluated_safer_directions += 1

        if not (f[preferred_direction]):
            return preferred_direction

        evaluated_unsafe_directions = 1
        while evaluated_unsafe_directions < 8:
            if clockwise:
                current_direction = (current_direction + 1) % 8
            else:
                current_direction = (current_direction - 1) % 8

            if not (f[current_direction]):
                return current_direction
            evaluated_unsafe_directions += 1
        
        return np.argmin(f)


    # This function receives the current state (r) of 
    # the system and returns the next state.
    # The current state (r) is an array of eight integers, 
    # r[i] := amount of rabbits in the i-th direction
    # state index, same as directions:
    # 0 1 2
    # 7   3
    # 6 5 4
    @staticmethod
    def chasing_1(r, preferred_direction, clockwise, diagonal_prediction):
        if not( np.any(r) ):
            return preferred_direction
        best_direction = np.argmax(r)
        neighbors = aux.get_neighbors(best_direction, clockwise)
        if aux.is_corner( best_direction ) or not( diagonal_prediction ):
            return neighbors[1]
        else:
            return aux.get_neighbors(neighbors[1], clockwise)[1]