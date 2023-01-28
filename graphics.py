import numpy as np
import pygame

import map

np.random.seed(1234)
pygame.display.init()

def create_system():

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    # For each cell:
    WIDTH = 30
    HEIGHT = 30
    MARGIN = 5

    # For the grid:
    ROWS = 15
    COLUMNS = 15

    # MAP CONSTANTS 
    INITIAL_RABBIT_POPULATION = 30
    INITIAL_FOX_POPULATION = 15


    # Preferred direction:
    # 0 1 2
    # 7   3
    # 6 5 4

    m1 = map.Map(ROWS, COLUMNS)
    m1.populate(INITIAL_RABBIT_POPULATION, 
        "rabbit", 
        "random", 
        preferred_direction = 5, 
        clockwise = True)
    m1.populate(INITIAL_FOX_POPULATION, "fox", "random")

    # [row, column, [rabbits, foxes]]
    grid = m1.get_population_map()
    grid.shape


    pygame.display.init()
    pygame.init()

    WINDOWS_SIZE = [1200, 600]
    screen = pygame.display.set_mode(WINDOWS_SIZE)
    pygame.display.set_caption("Rabbits & Foxes")

    done = False

    clock = pygame.time.Clock()


    FONT_SIZE = 16

    font = pygame.font.Font(None, FONT_SIZE)

    aux = 0
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     pos = pygame.mouse.get_pos()
            #     if ( pos[0] >= WIDTH * COLUMNS + MARGIN * (COLUMNS) 
            #         or pos[1] >= HEIGHT * ROWS + MARGIN * (ROWS) ):
            #         continue
            #     column = pos[0] // (WIDTH + MARGIN)
            #     row = pos[1] // (HEIGHT + MARGIN)
            #     grid[row, column, 0] = 1
            #     print("Click ", pos, "Grid coordinates: ", row, column)

        screen.fill(BLACK)

        for row in range(ROWS):
            for column in range(COLUMNS):
                color = WHITE
                if grid[row, column, 0] >= 1:
                    color = BLUE
                if grid[row, column, 1] >= 1:
                    color = RED
                pygame.draw.rect(screen,
                                color,
                                [(MARGIN + WIDTH) * column + MARGIN,
                                (MARGIN + HEIGHT) * row + MARGIN,
                                WIDTH,
                                HEIGHT])
                
                # render text onto a surface
                text_rabbits = font.render(f"R: {grid[row, column, 0]}", True, (0, 0, 0))
                # blit the surface onto the screen
                screen.blit(text_rabbits, [(MARGIN + WIDTH) * column 
                    + MARGIN , (MARGIN + HEIGHT) 
                    * row + MARGIN ])

                text_foxes = font.render(f"F: {grid[row, column, 1]}", True, (0, 0, 0))
                # blit the surface onto the screen
                screen.blit(text_foxes, [(MARGIN + WIDTH) * column 
                    + MARGIN , (MARGIN + HEIGHT) 
                    * row + MARGIN + FONT_SIZE ])

        # change color of the grid[0, 0] every two seconds
        
        if pygame.time.get_ticks() % 4000 < 2000:
            time_control = 0
            # grid[0,0,0] = 0
        else:
            time_control = 1
            # grid[0,0,0] = 1
        
        if aux != time_control:
            aux = time_control

            # m1.reproduction("rabbit")
            m1.hunt()
            m1.reproduction()
            m1.move_animals()
            grid = m1.get_population_map()


        clock.tick(60)

        pygame.display.flip()

    pygame.quit()




if __name__ == "__main__":
    create_system()


