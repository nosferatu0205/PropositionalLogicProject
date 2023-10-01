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


    def update(self, game_world: [[]], current_pos: (int, int), world: WumpusWorld) -> None:
        self.game_world = game_world
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
    def decide_next_move(self, current_pos: (int, int)) -> (int, int):
        # ekhane bfs or dfs diye highest point e jaoar try korbe with lowest number of steps, highest point and steps er number shoman hoile choose one randomly

    def find_valid_moves(self) -> [(int, int)]:
        # find all unvisited valid moves
