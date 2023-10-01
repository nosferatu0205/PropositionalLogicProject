import numpy as np
# from main import WumpusWorld
# Define the size of the arrays
WUMPUS_WORLD_SIZE = 10
array_size = (WUMPUS_WORLD_SIZE, WUMPUS_WORLD_SIZE)

class CellKnowledge:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pit = np.zeros(array_size, dtype=int)
        self.wumpus = np.zeros(array_size, dtype=int)
        self.gold = np.zeros(array_size, dtype=int)
        self.countBreezeSensedNearby = np.zeros(array_size, dtype=int)
        self.countStenchSensedNearby = np.zeros(array_size, dtype=int)
        self.countGlitterSensedNearby = np.zeros(array_size, dtype=int)
        self.visited = np.zeros(array_size, dtype=bool)  # Make 'visited' an array

        # Set the initial position (0, 0) as safe and visited
        if x == 0 and y == 0:
            self.visited[0, 0] = True

        self.knowledge_base = self.initialize_knowledge_base()

    def initialize_knowledge_base(self):
        knowledge_base = np.empty(array_size, dtype=object)

        for i in range(WUMPUS_WORLD_SIZE):
            for j in range(WUMPUS_WORLD_SIZE):
                knowledge_base[i, j] = CellKnowledge(i, j)

        return knowledge_base

    def update_knowledge_base(self, current_pos, knowledge_base):
            x , y = current_pos
            if x < 0 or y < 0 or x >= WUMPUS_WORLD_SIZE or y >= WUMPUS_WORLD_SIZE:
                return
            percepts = self.get_percepts(current_pos)
            for perceived in percepts:
                cell = knowledge_base[x, y]

                if perceived == 'BREEZE':
                    cell.countBreezeSensedNearby += 1
                elif perceived == 'STENCH':
                    cell.countStenchSensedNearby += 1
                elif perceived == 'GLITTER':
                    cell.countGlitterSensedNearby += 1

                # Update pit, wumpus, and gold based on perceptions
                if perceived == 'BREEZE':
                    cell.pit = 0
                elif perceived == 'STENCH':
                    cell.wumpus = 0
                elif perceived == 'GLITTER':
                    cell.gold = 0

    def predicate_glittery_and_safe_path(x, y, knowledge_base):
        if x < 0 or y < 0 or x >= WUMPUS_WORLD_SIZE or y >= WUMPUS_WORLD_SIZE:
            return False

        if (
            knowledge_base[x][y].countGlitterSensedNearby >= 1
            and not knowledge_base[x][y].pit
            and not knowledge_base[x][y].wumpus
        ):
            return True

        return False

    def predicate_safe_unvisited_path(x, y, knowledge_base):
        if x < 0 or y < 0 or x >= WUMPUS_WORLD_SIZE or y >= WUMPUS_WORLD_SIZE:
            return False

        if not knowledge_base[x][y].visited and not knowledge_base[x][y].pit and not knowledge_base[x][y].wumpus:
            return True

        return False

    def predicate_throw_arrow(x, y, knowledge_base, num_of_arrows):
        if x < 0 or y < 0 or x >= WUMPUS_WORLD_SIZE or y >= WUMPUS_WORLD_SIZE:
            return False

        if (knowledge_base[x][y].countStenchSensedNearby >= 2 and knowledge_base[x][y].countBreezeSensedNearby < 2 and num_of_arrows > 0):
            return True

        return False

    def exclude_death_paths(x, y, knowledge_base):
        less_dangerous_paths = []

        if (
            knowledge_base[x - 1][y].countBreezeSensedNearby < 2
            and knowledge_base[x - 1][y].countStenchSensedNearby < 2
        ):
            less_dangerous_paths.append((x - 1, y))
        elif (
            knowledge_base[x + 1][y].countBreezeSensedNearby < 2
            and knowledge_base[x + 1][y].countStenchSensedNearby < 2
        ):
            less_dangerous_paths.append((x + 1, y))
        elif (
            knowledge_base[x][y - 1].countBreezeSensedNearby < 2
            and knowledge_base[x][y - 1].countStenchSensedNearby < 2
        ):
            less_dangerous_paths.append((x, y - 1))
        elif (
            knowledge_base[x][y + 1].countBreezeSensedNearby < 2
            and knowledge_base[x][y + 1].countStenchSensedNearby < 2
        ):
            less_dangerous_paths.append((x, y + 1))

        return less_dangerous_paths

    def get_next_move(self,x, y, perceived,  num_of_arrows):
        self.knowledge_base[x][y].visited = True

        self.update_knowledge_base(x - 1, y, perceived, self.knowledge_base)
        self.update_knowledge_base(x + 1, y, perceived, self.knowledge_base)
        self.update_knowledge_base(x, y - 1, perceived, self.knowledge_base)
        self.update_knowledge_base(x, y + 1, perceived, self.knowledge_base)

        if self.predicate_glittery_and_safe_path(x + 1, y, self.knowledge_base):
            return x + 1, y
        elif self.predicate_glittery_and_safe_path(x - 1, y, self.knowledge_base):
            return x - 1, y
        elif self.predicate_glittery_and_safe_path(x, y + 1, self.knowledge_base):
            return x, y + 1
        elif self.predicate_glittery_and_safe_path(x, y - 1, self.knowledge_base):
            return x, y - 1

        if self.predicate_throw_arrow(x - 1, y, self.knowledge_base, num_of_arrows):
            return x - 1, y
        elif self.predicate_throw_arrow(x + 1, y, self.knowledge_base, num_of_arrows):
            return x + 1, y
        elif self.predicate_throw_arrow(x, y - 1, self.knowledge_base, num_of_arrows):
            return x, y - 1
        elif self.predicate_throw_arrow(x, y + 1, self.knowledge_base, num_of_arrows):
            return x, y + 1

        if self.predicate_safe_unvisited_path(x + 1, y, self.knowledge_base):
            return x + 1, y
        elif self.predicate_safe_unvisited_path(x - 1, y, self.knowledge_base):
            return x - 1, y
        elif self.predicate_safe_unvisited_path(x, y + 1, self.knowledge_base):
            return x, y + 1
        elif self.predicate_safe_unvisited_path(x, y - 1, self.knowledge_base):
            return x, y - 1

        # Backtrack since no visited safe path found
        if self.knowledge_base[x - 1][y].visited:
            return x - 1, y
        elif self.knowledge_base[x + 1][y].visited:
            return x + 1, y
        elif self.knowledge_base[x][y - 1].visited:
            return x, y - 1
        elif self.knowledge_base[x][y + 1].visited:
            return x, y + 1

        # We are back to cell (1,1). We have no other choice but to make a dangerous move
        # So we will list "probably dangerous" paths and pick one at random.
        probably_dangerous_paths = self.exclude_death_paths(x, y, self.knowledge_base)
        return probably_dangerous_paths[0]
