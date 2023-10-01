
from xml.dom import NotFoundErr
from Agent import Agent
from MyAI_2 import MyAI
import random
from wumpus_gui import *
import time
import sys

class World():
    
    # Tile Structure
    class __Tile:
        agent = False
        visited = False
        pit = False
        wumpus = False
        gold = False
        breeze = False
        stench = False

    def __init__ ( self, debug = False, file = None ):
        # Operation Flags
        self.__debug = debug

        
        # Agent Initialization
        self.__goldLooted = False
        self.__numberOfGolds = 0
        self.__hasArrow = True
        self.__numberOfArrows = 0
        self.__bump = False
        self.__scream = False
        self.__score = 0
        self.__agentDir = 0
        self.__agentX = 0
        self.__agentY = 0
        self.__lastAction = Agent.Action.CLIMB
        self.__board = NotFoundErr
        self.__colDimension = 10
        self.__rowDimension = 10
        self.__agent = None
            
        if file != None:
            self.__board = [[self.__Tile() for j in range(self.__rowDimension)] for i in range(self.__colDimension)]
            self.__addFeatures(file)
        else:
            
            self.__board = [[self.__Tile() for j in range(self.__colDimension)] for i in range(self.__rowDimension)]
            self.__addFeatures()

    def run ( self, screen ):
        self.__board[self.__agentX][self.__agentY].agent = True
        self.__board[self.__agentX][self.__agentY].visited = True
        wait_flag = False
        show_board = False
        while self.__score >= -1000:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        print('Space bar is pressed')
                        wait_flag = not wait_flag
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    show_board = not show_board

            if wait_flag:
                time.sleep(0.5)
                continue
            show_msg_up(str(self.__score), screen)
            show_percept(self.__board[self.__agentX][self.__agentY], self.__scream, screen)
            print(self.__scream)
            
            refresh_graphics(self.__board, self.__agentDir, show_board, screen)
            self.__board[self.__agentX][self.__agentY].agent = False

                        
            # Get the move
            self.__lastAction = self.__agent.getAction (self.__board[self.__agentX][self.__agentY].stench,self.__board[self.__agentX][self.__agentY].breeze,
														self.__board[self.__agentX][self.__agentY].gold, self.__bump, self.__scream)

            # Make the move
            self.__score -= 1
            self.__bump   = False
            self.__scream = False
            
            if self.__lastAction == Agent.Action.TURN_LEFT:
                self.__agentDir -= 1
                if (self.__agentDir < 0):
                    self.__agentDir = 3
                    
            elif self.__lastAction == Agent.Action.TURN_RIGHT:
                self.__agentDir += 1
                if self.__agentDir > 3:
                    self.__agentDir = 0
                    
            elif self.__lastAction == Agent.Action.FORWARD:
                if self.__agentDir == 0 and self.__agentX+1 < self.__colDimension:
                    self.__agentX += 1
                elif self.__agentDir == 1 and self.__agentY-1 >= 0:
                    self.__agentY -= 1
                elif self.__agentDir == 2 and self.__agentX-1 >= 0:
                    self.__agentX -= 1
                elif self.__agentDir == 3 and self.__agentY+1 < self.__rowDimension:
                    self.__agentY += 1
                else:
                    self.__bump = True
                    
                if self.__board[self.__agentX][self.__agentY].pit or self.__board[self.__agentX][self.__agentY].wumpus:
                    self.__score -= 10000
                    if self.__debug:
                        self.__printWorldInfo()
                    return self.__score
                
            elif self.__lastAction == Agent.Action.SHOOT:
            
                if self.__hasArrow:
                    self.__numberOfArrows-=1
                    if self.__numberOfArrows == 0:
                        self.__hasArrow = False
                    self.__score -= 10
                    
                    if self.__agentDir == 0:
                        for x in range (self.__agentX, self.__colDimension):
                                if self.__board[x][self.__agentY].wumpus:
                                    self.__board[x][self.__agentY].wumpus = False
                                    self.__board[x-1][self.__agentY].stench = False
                                    self.__board[x+1][self.__agentY].stench = False
                                    self.__board[x][self.__agentY+1].stench = False
                                    self.__board[x][self.__agentY-1].stench = False
                                    self.__scream = True
                                    
                    
                    elif self.__agentDir == 1:
                        for y in range (self.__agentY, -1, -1):
                            if self.__board[self.__agentX][y].wumpus:
                                self.__board[self.__agentX][y].wumpus = False

                                self.__board[self.__agentX-1][y].stench = False
                                self.__board[self.__agentX+1][y].stench = False
                                self.__board[self.__agentX][y+1].stench = False
                                self.__board[self.__agentX][y-1].stench = False
                                self.__scream = True
                    
                    elif self.__agentDir == 2:
                        for x in range (self.__agentX, -1, -1):
                            if self.__board[x][self.__agentY].wumpus:
                                self.__board[x][self.__agentY].wumpus = False
                                self.__board[x-1][self.__agentY].stench = False
                                self.__board[x+1][self.__agentY].stench = False
                                self.__board[x][self.__agentY+1].stench = False
                                self.__board[x][self.__agentY-1].stench = False
                                self.__scream = True

                    elif self.__agentDir == 3:
                        for y in range (self.__agentY, self.__rowDimension):
                            if self.__board[self.__agentX][y].wumpus:
                                self.__board[self.__agentX][y].wumpus = False

                                self.__board[self.__agentX-1][y].stench = False
                                self.__board[self.__agentX+1][y].stench = False
                                self.__board[self.__agentX][y+1].stench = False
                                self.__board[self.__agentX][y-1].stench = False
                                self.__scream = True
                    
            elif self.__lastAction == Agent.Action.GRAB:
                if self.__board[self.__agentX][self.__agentY].gold:
                    self.__board[self.__agentX][self.__agentY].gold = False
                    self.__numberOfGolds -= 1
                    if self.__numberOfGolds < 1:
                        self.__goldLooted = True
                    self.__score += 1000
                    
            elif self.__lastAction == Agent.Action.CLIMB:
                if self.__agentX == 0 and self.__agentY == 0:
                    if self.__goldLooted:
                        self.__score += 100
                    if (self.__debug):
                        self.__printWorldInfo()
                    return self.__score
            self.__board[self.__agentX][self.__agentY].visited = True
            self.__board[self.__agentX][self.__agentY].agent = True
        
        return self.__score
        

    #World Generation Functions

    
    def __addFeatures ( self, file = None ):
        if file == None:
            
            
            # Generate wumpus
            wc = self.__randomInt(self.__colDimension)
            wr = self.__randomInt(self.__rowDimension)
            
            while (wc == 0 or wc == 1) and (wr == 0 or wr == 1):
                wc = self.__randomInt(self.__colDimension)
                wr = self.__randomInt(self.__rowDimension)
                
            self.__addWumpus ( wc, wr )
            self.__numberOfArrows = 1
            
            # Generate gold
            gc = self.__randomInt(self.__colDimension)
            gr = self.__randomInt(self.__rowDimension)
                
            while ((gc == 0 or gc == 1) and (gr == 0 or gr == 1) and (self.__board[gc][gr].wumpus == True)):
                gc = self.__randomInt(self.__colDimension)
                gr = self.__randomInt(self.__rowDimension)
            
            self.__addGold ( gc, gr )
            self.__numberOfGolds = 1
            
            # Generate pits
            for r in range (self.__rowDimension):
                for c in range (self.__colDimension):
                    if (c != 0 or r != 0) and self.__randomInt(30) < 2 and (self.__board[c][r].wumpus == False) and (self.__board[c][r].gold == False):
                        self.__addPit ( c, r )

        else:
            for i in range (0,10):
                line = next(file).strip()
                char_list = list(line)
                # print(char_list)
                for j in range (0,10):
                    # print (i,j)
                    if char_list[j] == 'P':
                        self.__addPit(i, j)
                    elif char_list[j] == 'W':
                        self.__addWumpus(i, j)
                        self.__numberOfArrows+=1
                    elif char_list[j] == 'G':
                        self.__addGold(i,j)
                        self.__numberOfGolds += 1
                
            file.close()
        
        self.__agent = MyAI(self.__numberOfGolds, self.__numberOfArrows)
    
    def __addPit ( self, c, r ):
        if self.__isInBounds(c, r):
            self.__board[c][r].pit = True
            self.__addBreeze ( c+1, r )
            self.__addBreeze ( c-1, r )
            self.__addBreeze ( c, r+1 )
            self.__addBreeze ( c, r-1 )
    
    def __addWumpus ( self, c, r ):
        if self.__isInBounds(c, r):
            self.__board[c][r].wumpus = True
            self.__addStench ( c+1, r )
            self.__addStench ( c-1, r )
            self.__addStench ( c, r+1 )
            self.__addStench ( c, r-1 )
    
    def __addGold ( self, c, r ):
        if self.__isInBounds(c, r):
            self.__board[c][r].gold = True
    
    def __addStench ( self, c, r ):
        if self.__isInBounds(c, r):
            self.__board[c][r].stench = True
    
    def __addBreeze ( self, c, r ):
        if self.__isInBounds(c, r):
            self.__board[c][r].breeze = True
    
    def __isInBounds ( self, c, r ):
        return c < self.__colDimension and r < self.__rowDimension and c >= 0 and r >= 0
    

    # World Printing Functions

    
    def __printWorldInfo ( self ):
        self.__printBoardInfo()
        self.__printAgentInfo()
    
    def __printBoardInfo ( self ):
        for r in range (self.__rowDimension-1, -1, -1):
            for c in range (self.__colDimension):
                self.__printTileInfo ( c, r )
            print("")
            print("")

    def __printTileInfo ( self, c, r ):
        tileString = ""
        
        if self.__board[c][r].pit:    tileString += "P"
        if self.__board[c][r].wumpus: tileString += "W"
        if self.__board[c][r].gold:   tileString += "G"
        if self.__board[c][r].breeze: tileString += "B"
        if self.__board[c][r].stench: tileString += "S"
        
        if self.__agentX == c and self.__agentY == r:
            if self.__agentDir == 0:
                tileString += ">"
            
            elif self.__agentDir == 1:
                tileString += "v"
            
            elif self.__agentDir == 2:
                tileString += "<"
            
            elif self.__agentDir == 3:
                tileString += "^"
            #tileString += "@"
        
        tileString += "."
        
        print(tileString.rjust(8), end="")
    
    def __printAgentInfo ( self ):
        print ( "Score: "   + str(self.__score) )
        print ( "AgentX: "  + str(self.__agentX) )
        print ( "AgentY: "  + str(self.__agentY) )
        self.__printDirectionInfo()
        self.__printActionInfo()
        self.__printPerceptInfo()
    
    def __printDirectionInfo ( self ):
        if self.__agentDir == 0:
            print ( "AgentDir: Right" )
            
        elif self.__agentDir == 1:
            print ( "AgentDir: Down" )
            
        elif self.__agentDir == 2:
            print ( "AgentDir: Left" )
            
        elif self.__agentDir == 3:
            print ( "AgentDir: Up" )
            
        else:
            print ( "AgentDir: Invalid" )
    
    def __printActionInfo ( self ):
        if self.__lastAction == Agent.Action.TURN_LEFT:
            print ( "Last Action: Turned Left" )

        elif self.__lastAction == Agent.Action.TURN_RIGHT:
            print ( "Last Action: Turned Right")

        elif self.__lastAction == Agent.Action.FORWARD:
            print ( "Last Action: Moved Forward")

        elif self.__lastAction == Agent.Action.SHOOT:
            print ( "Last Action: Shot the Arrow")

        elif self.__lastAction == Agent.Action.GRAB:
            print ( "Last Action: Grabbed")

        elif self.__lastAction == Agent.Action.CLIMB:
            print ( "Last Action: Climbed")

        else:
            print ( "Last Action: Invalid")

    def __printPerceptInfo ( self ):
        perceptString = "Percepts: "
        
        if self.__board[self.__agentX][self.__agentY].stench: perceptString += "Stench, "
        if self.__board[self.__agentX][self.__agentY].breeze: perceptString += "Breeze, "
        if self.__board[self.__agentX][self.__agentY].gold:   perceptString += "Glitter, "
        if self.__bump:                         perceptString += "Bump, "
        if self.__scream:                       perceptString += "Scream"
        
        if perceptString[-1] == ' 'and perceptString[-2] == ',':
            perceptString = perceptString[:-2]
        
        print(perceptString)

    
    def __randomInt ( self, limit ):
        return random.randrange(limit)
