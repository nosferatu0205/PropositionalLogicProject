BREEZE = b'b'
STENCH = b's'
GLITTER = b'g'
PIT = b'p'
WUMPUS = b'w'
GOLD = b'$'
WUMPUS_WORLD_SIZE = 10

class CellKnowledge:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pit = True
        self.wumpus = True
        self.gold = True
        self.countBreezeSensedNearby = 0
        self.countStenchSensedNearby = 0
        self.countGlitterSensedNearby = 0
        self.visited = False

    def initialize_knowledge_base():
        knowledge_base = []
        for i in range(WUMPUS_WORLD_SIZE):
            row = []
            for j in range(WUMPUS_WORLD_SIZE):
                row.append(CellKnowledge(i, j))
            knowledge_base.append(row)
        return knowledge_base

    def update_knowledge_base(x, y, perceived_arr, knowledge_base):
        if x < 0 or y < 0 or x >= WUMPUS_WORLD_SIZE or y >= WUMPUS_WORLD_SIZE:
            return

        for perceived in perceived_arr:
            knowledge_base[x][y].pit ^= perceived == BREEZE
            knowledge_base[x][y].wumpus ^= perceived == STENCH
            knowledge_base[x][y].gold ^= perceived == GLITTER

            if perceived == BREEZE:
                knowledge_base[x][y].countBreezeSensedNearby += 1
            elif perceived == STENCH:
                knowledge_base[x][y].countStenchSensedNearby += 1
            elif perceived == GLITTER:
                knowledge_base[x][y].countGlitterSensedNearby += 1

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

        if (
            knowledge_base[x][y].countStenchSensedNearby >= 2
            and knowledge_base[x][y].countBreezeSensedNearby < 2
            and num_of_arrows > 0
        ):
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

    def get_next_move(x, y, perceived, knowledge_base, num_of_arrows):
        knowledge_base[x][y].visited = True

        update_knowledge_base(x - 1, y, perceived, knowledge_base)
        update_knowledge_base(x + 1, y, perceived, knowledge_base)
        update_knowledge_base(x, y - 1, perceived, knowledge_base)
        update_knowledge_base(x, y + 1, perceived, knowledge_base)

        if predicate_glittery_and_safe_path(x + 1, y, knowledge_base):
            return x + 1, y
        elif predicate_glittery_and_safe_path(x - 1, y, knowledge_base):
            return x - 1, y
        elif predicate_glittery_and_safe_path(x, y + 1, knowledge_base):
            return x, y + 1
        elif predicate_glittery_and_safe_path(x, y - 1, knowledge_base):
            return x, y - 1

        if predicate_throw_arrow(x - 1, y, knowledge_base, num_of_arrows):
            return x - 1, y
        elif predicate_throw_arrow(x + 1, y, knowledge_base, num_of_arrows):
            return x + 1, y
        elif predicate_throw_arrow(x, y - 1, knowledge_base, num_of_arrows):
            return x, y - 1
        elif predicate_throw_arrow(x, y + 1, knowledge_base, num_of_arrows):
            return x, y + 1

        if predicate_safe_unvisited_path(x + 1, y, knowledge_base):
            return x + 1, y
        elif predicate_safe_unvisited_path(x - 1, y, knowledge_base):
            return x - 1, y
        elif predicate_safe_unvisited_path(x, y + 1, knowledge_base):
            return x, y + 1
        elif predicate_safe_unvisited_path(x, y - 1, knowledge_base):
            return x, y - 1

        # Backtrack since no visited safe path found
        if knowledge_base[x - 1][y].visited:
            return x - 1, y
        elif knowledge_base[x + 1][y].visited:
            return x + 1, y
        elif knowledge_base[x][y - 1].visited:
            return x, y - 1
        elif knowledge_base[x][y + 1].visited:
            return x, y + 1

        # We are back to cell (1,1). We have no other choice but to make a dangerous move
        # So we will list "probably dangerous" paths and pick one at random.
        probably_dangerous_paths = exclude_death_paths(x, y, knowledge_base)
        return probably_dangerous_paths[0]
