import random
import pygame
import numpy
import DecisionMaker as ai2

# Define constants
WIDTH, HEIGHT = 800, 1000  # Increase the HEIGHT
GRID_SIZE = 10
CELL_SIZE = WIDTH // GRID_SIZE

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GOLD = (255, 215, 0)
BROWN = (139, 69, 19)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wumpus World")
font = pygame.font.Font(None, 32)
text = "Working?"
restart_button = pygame.Rect(325, 900, 150, 50)
change_view = pygame.Rect(60, 900, 180, 50)
# text_box = pygame.Rect(300, 820, 200, 50)
restart_color = BLACK
IMAGES = {}
wall_check = numpy.zeros((10,10), dtype=bool)
show_wall = True


arrows_display = pygame.Rect(575, 900, 150, 50)
points_display = pygame.Rect(325, 900, 200, 50)
percepts_display = pygame.Rect(75, 900, 400, 50)
#game_over_tracker = True


class WumpusWorld:
    def __init__(self, size=10, num_pits= 20, num_wumpus=2, num_gold =4):
        self.size = size
        self.num_gold = num_gold
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        self.agent_position = (0, 0)
        self.point =0
        self.num_wumpus = num_wumpus
        self.arrows = num_wumpus
        self.visited = set()
        self.num_pits = num_pits
        self.fallen_into_pit = False
        self.eaten_by_wumpus = False
        self.game_over_tracker = False
    def initialize(self):
        # Place the agent in the starting position
        self.agent_position = (0, 0)

        # Randomly place the gold
        gold_placed = 0
        while gold_placed < self.num_gold:
            # Randomly choose a position for a Wumpus
            gold_position = self.random_empty_position()

            # Check if the chosen position is not 1,2 and not 2,1, and it's not occupied by a pit
            if self.grid[gold_position[0]][gold_position[1]] != 'P' and self.grid[gold_position[0]][gold_position[1]] != 'W' and gold_position != (0,0):
                self.grid[gold_position[0]][gold_position[1]] = 'G'
                gold_placed += 1

        # Randomly place the Wumpus
        wumpus_placed = 0
        while wumpus_placed < self.num_wumpus:
            # Randomly choose a position for a Wumpus
            wumpus_position = self.random_empty_position()

            # Check if the chosen position is not 1,2 and not 2,1, and it's not occupied by a pit
            if wumpus_position != (0,0) and wumpus_position != (0,1) and wumpus_position != (1,0) and self.grid[wumpus_position[0]][wumpus_position[1]] != 'P':
                self.grid[wumpus_position[0]][wumpus_position[1]] = 'W'
                wumpus_placed += 1

        # Randomly add pits based on pit_probability
        pits_placed = 0
        while pits_placed < self.num_pits:
            # Randomly choose a position for a pit
            pit_position = self.random_empty_position()

            # Check if the chosen position is not 1,2 and not 2,1, and it's not occupied by a Wumpus
            if pit_position != (0, 0) and pit_position != (0, 1)  and pit_position != (1, 0) and self.grid[pit_position[0]][pit_position[1]] != 'W':
                self.grid[pit_position[0]][pit_position[1]] = 'P'
                pits_placed += 1

    def random_empty_position(self):
        while True:
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)
            if self.grid[row][col] is None:
                return (row, col)

    def move_agent(self, action):
        row, col = self.agent_position

        if action == 'left' and col > 0:
            self.agent_position = (row, col - 1)
            wall_check[row, col-1] = True
        elif action == 'right' and col < self.size - 1:
            self.agent_position = (row, col + 1)
            wall_check[row, col+1] = True
        elif action == 'up' and row > 0:
            self.agent_position = (row - 1, col)
            wall_check[row-1, col] = True
        elif action == 'down' and row < self.size - 1:
            self.agent_position = (row + 1, col)
            wall_check[row+1, col] = True

    def is_game_over(self, manualoverride =False):
        if manualoverride:
            self.game_over_tracker = True
            return True, "Game is over. agent climbed out."
        row, col = self.agent_position

        if self.grid[row][col] == 'W':
            if not self.eaten_by_wumpus:
                self.eaten_by_wumpus = True
                return True, "Agent was eaten by the Wumpus!"
        elif self.grid[row][col] == 'G':
            return False, "Agent found the gold and climbed out of the cave with +1000 points!"
        elif self.grid[row][col] == 'P':
            #self.text="Agent fell into a pit and lost 1000 points!"
            #return True, "Agent fell into a pit and lost 1000 points!"
            if not self.fallen_into_pit:
                self.fallen_into_pit = True
                self.point-=1000
                return True, "Agent fell into a pit and lost 1000 points!"
        return False, ""

    def get_percepts(self, position):
        row, col = position
        percepts = []

        # Check for Breeze (pit nearby)
        if row > 0 and self.grid[row - 1][col] == 'P':
            percepts.append('Breeze')
        if row < self.size - 1 and self.grid[row + 1][col] == 'P':
            percepts.append('Breeze')
        if col > 0 and self.grid[row][col - 1] == 'P':
            percepts.append('Breeze')
        if col < self.size - 1 and self.grid[row][col + 1] == 'P':
            percepts.append('Breeze')

        # Check for Stench (Wumpus nearby)
        if row > 0 and self.grid[row - 1][col] == 'W':
            percepts.append('Stench')
        if row < self.size - 1 and self.grid[row + 1][col] == 'W':
            percepts.append('Stench')
        if col > 0 and self.grid[row][col - 1] == 'W':
            percepts.append('Stench')
        if col < self.size - 1 and self.grid[row][col + 1] == 'W':
            percepts.append('Stench')

        # Check for Glint (gold nearby)
        if self.grid[row][col] == 'G':
            percepts.append('Glint')
        if row > 0 and self.grid[row - 1][col] == 'G':
            percepts.append('Glint')
        if row < self.size - 1 and self.grid[row + 1][col] == 'G':
            percepts.append('Glint')
        if col > 0 and self.grid[row][col - 1] == 'G':
            percepts.append('Glint')
        if col < self.size - 1 and self.grid[row][col + 1] == 'G':
            percepts.append('Glint')
            
        text = str(percepts)

        return percepts
    #
    # def print_world(self):
    #     for row in range(self.size):
    #         for col in range(self.size):
    #             if (row, col) == self.agent_position:
    #                 print("A", end=" ")
    #             elif self.grid[row][col] == 'G':
    #                 print("G", end=" ")
    #             elif self.grid[row][col] == 'W':
    #                 print("W", end=" ")
    #             elif self.grid[row][col] == 'P':
    #                 print("P", end=" ")
    #             else:
    #                 print("-", end=" ")
    #         print()
    #
    def draw_text(self, color, text, x, y):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        screen.blit(text_surface, text_rect)
        
    def draw_text2(self, color, text, x, y):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        x = (WIDTH - text_rect.width) // 2
        text_rect.topleft = (x, y)
        screen.blit(text_surface, text_rect)
        
    def draw(self, screen):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x = col * CELL_SIZE
                y = row * CELL_SIZE
                _rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                screen.blit(IMAGES["grass"], _rect)

                if (row, col) == self.agent_position:
                    screen.blit(IMAGES["agent_down"], _rect)
                elif self.grid[row][col] == 'G':
                    screen.blit(IMAGES["coin"], _rect)
                elif self.grid[row][col] == 'W':
                    screen.blit(IMAGES["wumpus"], _rect)
                    # pygame.draw.rect(screen, GOLD, (x+CELL_SIZE, y + CELL_SIZE, CELL_SIZE, CELL_SIZE), 5)
                elif self.grid[row][col] == 'P':
                    screen.blit(IMAGES["hole"], _rect)
                pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x = col * CELL_SIZE
                y = row * CELL_SIZE
                _rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                rect_right = pygame.Rect(x+CELL_SIZE, y, CELL_SIZE, CELL_SIZE)
                rect_left = pygame.Rect(x-CELL_SIZE, y, CELL_SIZE, CELL_SIZE)
                rect_up = pygame.Rect(x, y-CELL_SIZE, CELL_SIZE, CELL_SIZE)
                rect_down = pygame.Rect(x, y+CELL_SIZE, CELL_SIZE, CELL_SIZE)


                #gold er jonno
                if self.grid[row][col] == 'G':
                    img= "glitter"

                    # Check for gold in adjacent cells and draw glints
                    if col < 9:
                        screen.blit(IMAGES[img], rect_right)
                    if col > 0:
                        screen.blit(IMAGES[img], rect_left)
                    if row > 0:
                        screen.blit(IMAGES[img], rect_up)
                    if row < 9:
                        screen.blit(IMAGES[img], rect_down)


                # elif self.grid[row][col] == 'G':
                    # screen.blit(IMAGES["coin"], _rect)
                if self.grid[row][col] == 'W':
                    img = "smell"
                    if col < 9:
                        screen.blit(IMAGES[img], rect_right)
                    if col > 0:
                        screen.blit(IMAGES[img], rect_left)
                    if row > 0:
                        screen.blit(IMAGES[img], rect_up)
                    if row < 9:
                        screen.blit(IMAGES[img], rect_down)
                    # pygame.draw.rect(screen, GOLD, (x+CELL_SIZE, y + CELL_SIZE, CELL_SIZE, CELL_SIZE), 5)
                elif self.grid[row][col] == 'P':
                    img = "breeze"
                    if col < 9:
                        screen.blit(IMAGES[img], rect_right)
                    if col > 0:
                        screen.blit(IMAGES[img], rect_left)
                    if row > 0:
                        screen.blit(IMAGES[img], rect_up)
                    if row < 9:
                        screen.blit(IMAGES[img], rect_down)
                pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)

        if show_wall:
            for row in range(GRID_SIZE):
                for col in range(GRID_SIZE):
                    x = col * CELL_SIZE
                    y = row * CELL_SIZE
                    _rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                    if (row != 0 or col != 0) and wall_check[row,col] == False :
                       screen.blit(IMAGES["wall"], _rect)
        # pygame.draw.rect(screen, BLACK, text_box)
        # pygame.draw.rect(screen, GREEN, text_box, 2)
        self.draw_text2( BLACK ,text, 360, 825)

        # Draw the restart button
        pygame.draw.rect(screen, restart_color, change_view)
        pygame.draw.rect(screen, BLACK, change_view, 2)
        pygame.draw.rect(screen, restart_color, restart_button)
        pygame.draw.rect(screen, BLACK, restart_button, 2)

        #pygame.draw.rect(screen, WHITE, arrows_display)
        #pygame.draw.rect(screen, WHITE, arrows_display, 2)
        self.draw_text(BLACK, f"Arrows Left: {self.arrows}", 575, 900)

        self.draw_text(BLACK, f"Gold remaining: {self.num_gold}", 575, 875)
        # self.draw_text(BLACK, f"Controls:", 25, 825)

        # self.draw_text(BLACK, f"Navigation:", 25, 850)

        # self.draw_text(BLACK, f"Up - down - left - right", 25, 875)
        # self.draw_text(BLACK, f"G - pick up gold", 25, 900)
        # self.draw_text(BLACK, f"0 - Climb out", 25, 925)
        # self.draw_text(BLACK, f"Shoot Wumpus", 25, 950)
        # self.draw_text(BLACK, f"Press W, A, S, D while facing wumpus", 25, 975)
        
        #pygame.draw.rect(screen, WHITE, points_display)
        #pygame.draw.rect(screen, WHITE, points_display, 2)
        self.draw_text(BLACK, f"Points: {self.point}", 575, 925)
        self.draw_text(BLACK, f"Wumpus left: {self.num_wumpus}", 575, 850)

        # pygame.draw.rect(screen, WHITE, percepts_display)
        # pygame.draw.rect(screen, BLACK, percepts_display, 2)
        # percepts = self.get_percepts(self.agent_position)
        # #self.draw_text(BLACK, f"Percepts: {', '.join(percepts)}", 575, 825)

        self.draw_text( GREEN ,"Restart", 363, 914)
        self.draw_text( GREEN ,"Change View", 76, 914)

    def print_world(self):
        for row in range(self.size):
            for col in range(self.size):
                if (row, col) == self.agent_position:
                    print("A", end=" ")
                elif self.grid[row][col] == 'G':
                    print("G", end=" ")
                elif self.grid[row][col] == 'W':
                    print("W", end=" ")
                elif self.grid[row][col] == 'P':
                    print("P", end=" ")
                else:
                    print("-", end=" ")
            print()

def load_images():
    # wumpus er age wall chhilo
    pics = ["agent_down", "agent_left", "agent_right", "agent_up", "breeze", "coin", "glitter", "grass", "hole", "smell", "wumpus" , "wumpus_dead", "wall"]
    for pic in pics:
        IMAGES[pic] = pygame.transform.scale(pygame.image.load(f"./Asset/{pic}.png"), (CELL_SIZE, CELL_SIZE))
    

# Main game loop
if __name__ == "__main__":
    load_images()
    world = WumpusWorld()
    decision_maker = ai2.DecisionMaker()
    world.initialize()
    running = True

    while running:
        screen.fill(WHITE)
        world.draw(screen)
        pygame.display.flip()

        game_over, result_message = world.is_game_over()
        row, col = world.agent_position
        perceived_info = world.get_percepts(world.agent_position)
        # cell_knowledge = ai.CellKnowledge(row,col)
        # next_x, next_y = ai.cell_knowledge.get_next_move(row, col, perceived_info, world.arrows)
        # print(next_x, next_y)
        # #ai =ai.CellKnowledge(row, col)
        # percepts= world.get_percepts(world.agent_position)


# Call the find_valid_moves() method on the instance

        #print(ai.get_next_move(row,col, percepts, world.arrows))
    # Get the next action from the AI#
        #print(ai.getNextMove())
        #ai.printPath()

        #if result_message == "Agent fell into a pit and lost 1000 points!":
            #world.point-=1000
        if game_over:
            world.game_over_tracker = True
            print("\nGame Over:", result_message)
            # running= False

            wall_check = numpy.ones((10, 10), dtype=bool)
            # world = WumpusWorld()
            # world.initialize()
            text = "Agent died. Game over. Press restart to try again."

            # todo: game over hoile game theke ber hoye jay, eita solve korte hobe - done


       # print("\nCurrent world:")
       # for row in range(GRID_SIZE):
          #  print(" ".join(world.grid[row]))

       # game_over, result_message = world.is_game_over()
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                world.print_world()

                decision_maker.update(world.agent_position, world)
                valid_moves = decision_maker.find_valid_moves(world.agent_position)
# Now, valid_moves contains a list of valid moves as (row, col) tuples
                print("valid moves", decision_maker.find_valid_moves(world.agent_position))
                if world.game_over_tracker:
                    continue
                if event.key == pygame.K_w or event.key == pygame.K_s or event.key == pygame.K_d or event.key == pygame.K_a:
                    row, col = world.agent_position
                    if event.key == pygame.K_w and world.grid[row-1][col] == 'W' and world.arrows>0:
                        world.grid[row-1][col] = None
                        world.num_wumpus -=1
                        world.point-=10
                        world.arrows-=1
                        print("Agent killed the Wumpus!")
                    elif event.key == pygame.K_s and world.grid[row+1][col] == 'W' and  world.arrows>0:
                        world.grid[row+1][col] = None
                        world.num_wumpus -=1
                        world.point-=10
                        world.arrows-=1
                        print("Agent killed the Wumpus!")
                    elif event.key == pygame.K_d and world.grid[row][col+1] == 'W' and  world.arrows>0:
                        world.grid[row][col+1] = None
                        world.num_wumpus -=1
                        world.point-=10
                        world.arrows-=1
                        print("Agent killed the Wumpus!")
                    elif event.key == pygame.K_a and world.grid[row][col-1] == 'W' and  world.arrows>0:
                        world.grid[row][col-1] = None
                        world.num_wumpus -=1
                        world.point-=10
                        world.arrows-=1
                        print("Agent killed the Wumpus!")

                elif event.key == pygame.K_LEFT:
                    world.move_agent('left')
                    world.point-=1
                elif event.key == pygame.K_RIGHT:
                    world.move_agent('right')
                    world.point-=1
                elif event.key == pygame.K_UP:
                    world.move_agent('up')
                    world.point-=1
                elif event.key == pygame.K_DOWN:
                    world.move_agent('down')
                    world.point-=1

                elif event.key == pygame.K_0 and world.agent_position == (0, 0):
                    running = False
                elif event.key == pygame.K_g:
                    # Allow the agent to pick up gold when 'G' key is pressed
                    row, col = world.agent_position
                    if world.grid[row][col] == 'G':
                        world.grid[row][col] = None  # Remove gold from the current cell
                        world.num_gold -= 1
                        world.point += 1000
                print("Arrows left:", world.arrows)
                percepts = list(set(world.get_percepts(world.agent_position)))
                text = str(percepts)
                print("Percepts:", percepts)
                print("points: ", world.point)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if restart_button.collidepoint(event.pos):
                        # Restart the game when the restart button is clicked
                        wall_check = numpy.zeros((10, 10), dtype=bool)
                        world = WumpusWorld()
                        world.initialize()
                        text = "restarted"
            
                    elif change_view.collidepoint(event.pos):
                        print("changed")
                        show_wall = not show_wall




    pygame.quit()
