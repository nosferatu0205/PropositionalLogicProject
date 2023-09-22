import random
import pygame

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
font = pygame.font.Font(None, 36)
text = "Working?"
restart_button = pygame.Rect(325, 900, 150, 50)
# text_box = pygame.Rect(300, 820, 200, 50)
restart_color = BLACK


class WumpusWorld:
    def __init__(self, size=10, num_pits= 20, num_wumpus=5, num_gold =4):
        self.size = size
        self.num_gold = num_gold
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        self.agent_position = (0, 0)
        self.point =0
        self.num_wumpus = num_wumpus
        self.arrows = 1
        self.visited = set()
        self.num_pits = num_pits

    def initialize(self):
        # Place the agent in the starting position
        self.agent_position = (0, 0)
        self.arrows = 1

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
        elif action == 'right' and col < self.size - 1:
            self.agent_position = (row, col + 1)
        elif action == 'up' and row > 0:
            self.agent_position = (row - 1, col)
        elif action == 'down' and row < self.size - 1:
            self.agent_position = (row + 1, col)




    def shoot_arrow(self):
        if self.arrows > 0:
            self.arrows -= 1
            row, col = self.agent_position

            if self.grid[row][col] == 'W':
                return True  # Wumpus is killed
            else:
                return False  # Arrow missed
        else:
            return False  # No arrows left
    def is_game_over(self, manualoverride =False):
        if manualoverride:
            return True, "Game is over"
        row, col = self.agent_position

        if self.grid[row][col] == 'W':
            return True, "Agent was eaten by the Wumpus!"
        elif self.grid[row][col] == 'G':
            return False, "Agent found the gold and climbed out of the cave with +1000 points!"
        elif self.grid[row][col] == 'P':
            return True, "Agent fell into a pit and lost -1000 points!"
        elif self.arrows == 0 and 'W' in [self.grid[r][c] for r, c in self.get_adjacent_cells(row, col)]:
            return True, "Agent ran out of arrows and couldn't kill the Wumpus."



        return False, ""

    def get_percepts(self):
        row, col = self.agent_position
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
            
        text = str(percepts)

        return percepts

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

                if (row, col) == self.agent_position:
                    pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE))
                    pygame.draw.circle(screen, GREEN, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 3)
                elif self.grid[row][col] == 'G':
                    pygame.draw.rect(screen, GOLD, (x, y, CELL_SIZE, CELL_SIZE))
                elif self.grid[row][col] == 'W':
                    pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE))
                    pygame.draw.circle(screen, BLACK, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 3)
                elif self.grid[row][col] == 'P':
                    pygame.draw.rect(screen, BROWN, (x, y, CELL_SIZE, CELL_SIZE))
                else:
                    pygame.draw.rect(screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)
                
        # pygame.draw.rect(screen, BLACK, text_box)
        # pygame.draw.rect(screen, GREEN, text_box, 2)
        self.draw_text2( BLACK ,text, 360, 825)        

        # Draw the restart button
        pygame.draw.rect(screen, restart_color, restart_button)
        pygame.draw.rect(screen, BLACK, restart_button, 2)
        self.draw_text( GREEN ,"Restart", 360, 914)

    def shoot_arrow(self):
        if self.arrows > 0:
            self.arrows -= 1
            row, col = self.agent_position

            if self.grid[row][col] == 'W':
                return True  # Wumpus is killed
            else:
                return False  # Arrow missed
        else:
            return False  # No arrows left

# Main game loop
if __name__ == "__main__":
    world = WumpusWorld()
    world.initialize()
    running = True
    while running:
        screen.fill(WHITE)
        world.draw(screen)
        pygame.display.flip()
        game_over, result_message = world.is_game_over()

        if result_message == "Agent fell into a pit and lost -1000 points!":
            world.point-=1000
        if game_over:
            print("\nGame Over:", result_message)
            running= False
            # todo: game over hoile game theke ber hoye jay, eita solve korte hobe

        print("\nCurrent world:")
       # for row in range(GRID_SIZE):
          #  print(" ".join(world.grid[row]))
        print("Arrows left:", world.arrows)
        percepts = list(set(world.get_percepts()))
        text = str(percepts)
        print("Percepts:", percepts)
        print("points: ", world.point)
       # game_over, result_message = world.is_game_over()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
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
                elif event.key == pygame.K_SPACE:
                    wumpus_killed = world.shoot_arrow()
                    world.point-=10
                    if wumpus_killed:
                        print("Agent killed the Wumpus!")
                elif event.key == pygame.K_0 and world.agent_position == (0, 0):
                    running = False
                elif event.key == pygame.K_g:
                    # Allow the agent to pick up gold when 'G' key is pressed
                    row, col = world.agent_position
                    if world.grid[row][col] == 'G':
                        world.grid[row][col] = None  # Remove gold from the current cell
                        world.num_gold -= 1
                        world.point += 1000


            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if restart_button.collidepoint(event.pos):
                        # Restart the game when the restart button is clicked
                        world = WumpusWorld()
                        world.initialize()
                        text = "restarted"




    pygame.quit()
