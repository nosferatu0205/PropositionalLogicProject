from main import WumpusWorld

UNKNOWN_SPACE = 100
GAME_WIDTH = 10
GAME_HEIGHT = 10
VISITED_SPACE = 2
STENCH_REDUCED_SCORE = 5
BREEZE_REDUCED_SCORE = 5


class DecisionMaker:
    def __init__(self) -> None:
        self.game_world = [[UNKNOWN_SPACE for i in range(GAME_WIDTH)] for j in range(GAME_HEIGHT)] # 10 means unknown
        self.visited = [[False for i in range(GAME_WIDTH)] for j in range(GAME_HEIGHT)] # False means not visited


    def update(self,  current_pos: (int, int), world: WumpusWorld) -> None:
        game_world = self.game_world
        game_world[current_pos[0]][current_pos[1]] = VISITED_SPACE # 2 means visited
        self.visited[current_pos[0]][current_pos[1]] = True

        # update scores based on percepts
        percepts = world.get_percepts(current_pos)
        # get_percepts = [stench, breeze, glitter]
        for each_percept in percepts:
            if each_percept == 'stench':
                self.reduce_score(current_pos, STENCH_REDUCED_SCORE)
            elif each_percept == 'breeze':
                self.reduce_score(current_pos, BREEZE_REDUCED_SCORE)
            # todo: decide glitter logic. Maybe we should add more value to glitter
            elif each_percept == 'glitter':
                self.reduce_score(current_pos, 0)

    def reduce_score(self, current_pos: (int, int), offset: int) -> None:
        # corresponding col update
        if current_pos[0] == 0:
            if not self.visited[current_pos[0]+1][current_pos[1]]:
                self.game_world[current_pos[0]+1][current_pos[1]] -= offset
        elif current_pos[0] == 9:
            if not self.visited[current_pos[0]-1][current_pos[1]]:
                self.game_world[current_pos[0]-1][current_pos[1]] -= offset
        else:
            if not self.visited[current_pos[0]+1][current_pos[1]]:
                self.game_world[current_pos[0]+1][current_pos[1]] -= offset
            if not self.visited[current_pos[0]-1][current_pos[1]]:
                self.game_world[current_pos[0]-1][current_pos[1]] -= offset

        # corresponding row update
        if current_pos[1] == 0:
            if not self.visited[current_pos[0]][current_pos[1]+1]:
                self.game_world[current_pos[0]][current_pos[1]+1] -= offset
        elif current_pos[1] == 9:
            if not self.visited[current_pos[0]][current_pos[1]-1]:
                self.game_world[current_pos[0]][current_pos[1]-1] -= offset
        else:
            if not self.visited[current_pos[0]][current_pos[1]+1]:
                self.game_world[current_pos[0]][current_pos[1]+1] -= offset
            if not self.visited[current_pos[0]][current_pos[1]-1]:
                self.game_world[current_pos[0]][current_pos[1]-1] -= offset


    # decide where to go next
    #def decide_next_move(self, current_pos: (int, int)) -> (int, int):
        # ekhane bfs or dfs diye highest point e jaoar try korbe with lowest number of steps, highest point and steps er number shoman hoile choose one randomly

    # def find_valid_moves(self, current_pos: (int, int)) -> [(int, int)]:
    #     valid_moves = []
    #     valid_paths= []
    #     visitedbydfs = set()
    #     rows = 10
    #     cols = 10
    #     dirs = [[0, 1], [0, -1], [1, 0], [-1, 0]]
    #     import collections
    #     def dfs(r, c):
    #         q = collections.deque()
    #         q.append((r, c))
    #
    #
    #         while q:
    #             rowO, colO = q.pop()
    #
    #             for dx, dy in dirs:
    #                 row = dx + rowO
    #                 col = dy + colO
    #
    #                 if(row in range(rows) and col in range(cols) and (row, col) not in visitedbydfs and self.visited[row][col] == True):
    #                     visitedbydfs.add((row, col))
    #                     q.append((row, col))
    #
    #
    #     for r in range(rows):
    #         for c in range(cols):
    #
    #             if (r, c) not in visited and grid[r][c] == "1":
    #
    #                 dfs(r, c)
    #                 count += 1
    #
    #     return count
    def dfs(self, current_pos: (int, int)) -> [(int, int)]:

        valid_moves = []

        self.visited.add(current_pos)
        row, col = current_pos

        # Define the possible moves: right, left, down, up
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dr, dc in moves:
            new_row, new_col = row + dr, col + dc
            new_position = (new_row, new_col)

            # Check if the new position is within the game bounds
            if 0 <= new_row < GAME_HEIGHT and 0 <= new_col < GAME_WIDTH:
                # Check if the new position is unvisited
                if not self.visited[new_row][new_col]:
                    valid_moves.append(new_position)
                    if new_position not in self.visited:
                        dfs(new_position)

       # Start DFS from all visited positions
        for row in range(GAME_HEIGHT):
            for col in range(GAME_WIDTH):
                if self.visited[row][col]:
                    dfs((row, col))

        return valid_moves

    def find_valid_moves(self, current_pos: (int, int)) -> [(int, int)]:
        valid_moves = []
        visitedbydfs = set()

        def dfs(position):
            visitedbydfs.add(position)
            row, col = position

            # Define the possible moves: right, left, down, up
            moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]

            for dr, dc in moves:
                new_row, new_col = row + dr, col + dc
                new_position = (new_row, new_col)

                # Check if the new position is within the game bounds
                if 0 <= new_row < GAME_HEIGHT and 0 <= new_col < GAME_WIDTH:
                    # Check if the new position is unvisited
                    if not visitedbydfs[new_row][new_col]:
                        valid_moves.append(new_position)
                        if self.visited[new_position[0]][new_position[1]] == True:
                            dfs(new_position)

        # Start DFS from all visited positions
        for row in range(GAME_HEIGHT):
            for col in range(GAME_WIDTH):
                if self.visited[row][col]:
                    dfs((row, col))

        return valid_moves






