import random
import pygame

# Define constants
WIDTH, HEIGHT = 800, 800
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



class WumpusWorld:
    def __init__(self, size=10, pit_probability=0.2):
        self.size = size
        self.pit_probability = pit_probability
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        self.agent_position = (0, 0)
        self.gold_position = None
        self.wumpus_position = None
        self.arrows = 1
        self.visited = set()

    def initialize(self):
        # Place the agent in the starting position
        self.agent_position = (0, 0)
        self.arrows = 1

        # Randomly place the gold
        self.gold_position = self.random_empty_position()

        # Randomly place the Wumpus
        self.wumpus_position = self.random_empty_position()

        # Randomly add pits based on pit_probability
        for row in range(self.size):
            for col in range(self.size):
                if (row, col) != self.agent_position and (row, col) != self.gold_position and (row, col) != self.wumpus_position:
                    if random.random() < self.pit_probability:
                        self.grid[row][col] = 'P'

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

            if (row, col) == self.wumpus_position:
                return True  # Wumpus is killed
            else:
                return False  # Arrow missed
        else:
            return False  # No arrows left

    def is_game_over(self):
        row, col = self.agent_position

        if (row, col) == self.wumpus_position:
            return True, "Agent was eaten by the Wumpus!"
        elif (row, col) == self.gold_position:
            return True, "Agent found the gold and climbed out of the cave with +1000 points!"
        elif self.grid[row][col] == 'P':
            return True, "Agent fell into a pit and lost -1000 points!"
        elif self.arrows == 0 and (row, col) != self.wumpus_position:
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
        if (row > 0 and self.wumpus_position == (row - 1, col)) or \
           (row < self.size - 1 and self.wumpus_position == (row + 1, col)) or \
           (col > 0 and self.wumpus_position == (row, col - 1)) or \
           (col < self.size - 1 and self.wumpus_position == (row, col + 1)):
            percepts.append('Stench')

        # Check for Glint (gold nearby)
        if (row > 0 and self.gold_position == (row - 1, col)) or \
           (row < self.size - 1 and self.gold_position == (row + 1, col)) or \
           (col > 0 and self.gold_position == (row, col - 1)) or \
           (col < self.size - 1 and self.gold_position == (row, col + 1)):
            percepts.append('Glint')

        return percepts

    def print_world(self):
        for row in range(self.size):
            for col in range(self.size):
                if (row, col) == self.agent_position:
                    print("A", end=" ")
                elif (row, col) == self.gold_position:
                    print("G", end=" ")
                elif (row, col) == self.wumpus_position:
                    print("W", end=" ")
                elif self.grid[row][col] == 'P':
                    print("P", end=" ")
                else:
                    print("-", end=" ")
            print()
    def draw(self, screen):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x = col * CELL_SIZE
                y = row * CELL_SIZE

                if (row, col) == self.agent_position:
                    pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE))
                    pygame.draw.circle(screen, GREEN, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 3)
                elif (row, col) == self.gold_position:
                    pygame.draw.rect(screen, GOLD, (x, y, CELL_SIZE, CELL_SIZE))
                elif (row, col) == self.wumpus_position:
                    pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE))
                    pygame.draw.circle(screen, BLACK, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 3)
                elif self.grid[row][col] == 'P':
                    pygame.draw.rect(screen, BROWN, (x, y, CELL_SIZE, CELL_SIZE))
                else:
                    pygame.draw.rect(screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)

    def move_agent(self, action):
        row, col = self.agent_position

        if action == 'left' and col > 0:
            self.agent_position = (row, col - 1)
        elif action == 'right' and col < GRID_SIZE - 1:
            self.agent_position = (row, col + 1)
        elif action == 'up' and row > 0:
            self.agent_position = (row - 1, col)
        elif action == 'down' and row < GRID_SIZE - 1:
            self.agent_position = (row + 1, col)

        self.visited.add(self.agent_position)

    def shoot_arrow(self):
        if self.arrows > 0:
            self.arrows -= 1
            row, col = self.agent_position

            if (row, col) == self.wumpus_position:
                return True  # Wumpus is killed
            else:
                return False  # Arrow missed
        else:
            return False  # No arrows left

    def is_game_over(self):
        row, col = self.agent_position

        if (row, col) == self.gold_position:
            return True, "Agent found the gold and climbed out of the cave with +1000 points!"
        elif self.grid[row][col] == 'P':
            return True, "Agent fell into a pit and lost -1000 points!"
        elif (row, col) == self.wumpus_position:
            return True, "Agent was eaten by the Wumpus."
        elif self.arrows == 0 and (row, col) != self.wumpus_position:
            return True, "Agent ran out of arrows and couldn't kill the Wumpus."

        return False, ""

    def get_percepts(self):
        percepts = []

        row, col = self.agent_position

        # Check for Breeze (pit nearby)
        if (row > 0 and self.grid[row - 1][col] == 'P') or \
           (row < GRID_SIZE - 1 and self.grid[row + 1][col] == 'P') or \
           (col > 0 and self.grid[row][col - 1] == 'P') or \
           (col < GRID_SIZE - 1 and self.grid[row][col + 1] == 'P'):
            percepts.append('Breeze')

        # Check for Stench (Wumpus nearby)
        if (row > 0 and self.wumpus_position == (row - 1, col)) or \
           (row < GRID_SIZE - 1 and self.wumpus_position == (row + 1, col)) or \
           (col > 0 and self.wumpus_position == (row, col - 1)) or \
           (col < GRID_SIZE - 1 and self.wumpus_position == (row, col + 1)):
            percepts.append('Stench')

        # Check for Glitter (gold nearby)
        if (row, col) == self.gold_position:
            percepts.append('Glitter')

        return percepts
# Main game loop
if __name__ == "__main__":
    world = WumpusWorld()
    world.initialize()
    running = True
    while running:
        screen.fill(WHITE)
        world.draw(screen)
        pygame.display.flip()
        print("\nCurrent world:")
       # for row in range(GRID_SIZE):
          #  print(" ".join(world.grid[row]))
        print("Arrows left:", world.arrows)
        percepts = world.get_percepts()
        print("Percepts:", percepts)
        game_over, result_message = world.is_game_over()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    world.move_agent('left')
                elif event.key == pygame.K_RIGHT:
                    world.move_agent('right')
                elif event.key == pygame.K_UP:
                    world.move_agent('up')
                elif event.key == pygame.K_DOWN:
                    world.move_agent('down')
                elif event.key == pygame.K_SPACE:
                    wumpus_killed = world.shoot_arrow()
                    if wumpus_killed:
                        print("Agent killed the Wumpus!")
                elif world.is_game_over():
                    game_over, result_message = world.is_game_over()
                    print("\nGame Over:", result_message)




    pygame.quit()
