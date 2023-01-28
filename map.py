import numpy as np
import copy

import aux
import animal

class Map:

    def __init__(self, _rows, _cols, _fox_starving_time = 4,
            _rabbit_reproduction_time = 3):
        self.species_list = ["rabbit", "fox"]
        self.rows = _rows
        self.cols = _cols
        self.population_map = np.zeros(
            (self.rows, self.cols, len(self.species_list) ), dtype = int)

        self.objects_map = [[[[], []] 
                for i in range(self.cols)] for j in range(self.rows)]
        self.hunt_log_map = np.zeros((self.rows, self.cols), dtype = int)

        self.time = 0
        self.fox_starving_time = _fox_starving_time
        self.rabbit_reproduction_time = _rabbit_reproduction_time


    def get_population_map(self):
        return self.make_population_map()


    def get_objects_map(self):
        return self.objects_map


    def set_population_map(self, _population_map):
        self.population_map = _population_map


    def set_objects_map(self, _objects_map):
        self.objects_map = _objects_map


    def populate(self, amount, species, strategy, 
        preferred_direction = None, clockwise = True,
        diagonal_prediction = False):

        self.hunt_log_map = np.zeros((self.rows, self.cols), dtype = int)

        if not (species == "rabbit" or species == "fox"):
            raise ValueError("invalid animal species")

        if species == "rabbit":
            species_index = 0
        elif species == "fox":
            species_index = 1

        for i in range (amount):
            row = np.random.randint(0, self.rows)
            col = np.random.randint(0, self.cols)
            self.objects_map[row][col][species_index].append(
                animal.Animal(
                row, col, species, strategy, preferred_direction, 
                clockwise, diagonal_prediction))
        self.make_population_map()

    def move_animals(self):
        self.make_population_map()
        
        for i in range(self.rows):
            for j in range(self.cols):
                for species_index in range( len(self.species_list) ):
                    for animal in self.objects_map[i][j][species_index]:
                        rabbits_around = None
                        foxes_around = None
                        if animal.species == "rabbit":
                            if species_index != 0:
                                raise ValueError("invalid animal index")
                            foxes_around = aux.get_animals_around(self.population_map, 
                                i, j, "fox" )
                        elif (animal.species == "fox"):
                            if species_index != 1:
                                raise ValueError("invalid animal index")
                            if animal.get_moves_without_eating() > self.fox_starving_time:
                                self.objects_map[i][j][species_index].remove(animal)
                                continue
                            rabbits_around = aux.get_animals_around(self.population_map, 
                                i, j, "rabbit" )

                        animal.move( (self.rows, self.cols, len(self.species_list)), 
                            rabbits_around, foxes_around )
                        self.objects_map[animal.row][animal.col][species_index].append(animal)
                        self.objects_map[i][j][species_index].remove(animal)
        self.time += 1


    def make_population_map(self):
        self.population_map = np.zeros(
            (self.rows, self.cols, len(self.species_list) ), dtype = int)

        for i in range(self.rows):
            for j in range(self.cols):
                for species_index in range( len(self.species_list) ):
                    self.population_map[i, j, species_index] \
                        = len(self.objects_map[i][j][species_index])
        return self.population_map


    def hunt(self):
        self.hunt_log_map = np.zeros((self.rows, self.cols), dtype = int)
        for i in range(self.rows):
            for j in range(self.cols):
                rabbits_array = self.objects_map[i][j][0]
                foxes_array = self.objects_map[i][j][1]

                hunted_animals = min( len(foxes_array), len(rabbits_array) )
                self.objects_map[i][j][0] = list (np.delete(
                        rabbits_array, np.random.choice(len(rabbits_array), 
                    hunted_animals, replace = False)))
                self.hunt_log_map[i, j] += hunted_animals


    def reproduction(self):
        temporal_objects_map = copy.deepcopy(self.objects_map)

        species = "fox"
        species_index = self.species_list.index(species)
        for i in range(self.rows):
            for j in range(self.cols):
                if (self.objects_map[i][j][species_index]):
                    breeding_foxes = list( np.random.choice(
                        self.objects_map[i][j][species_index],
                        self.hunt_log_map[i, j],
                        replace = False ) )
                    for fox in breeding_foxes:
                        brood = fox.reproduce()
                        self.objects_map[brood.row][brood.col][species_index] \
                            .append(fox.reproduce())

        # temporal_objects_map = copy.deepcopy(self.objects_map)

        species = "rabbit"
        species_index = self.species_list.index(species)
        # if (int(self.time) % int(self.rabbit_reproduction_time) == 0):
        for i in range(self.rows):
            for j in range(self.cols):
                if len(temporal_objects_map[i][j][species_index]) == 0:
                    continue
                for animal in temporal_objects_map[i][j][species_index]:
                    brood = animal.reproduce()
                    self.objects_map[brood.row][brood.col][species_index] \
                        .append(animal.reproduce())
