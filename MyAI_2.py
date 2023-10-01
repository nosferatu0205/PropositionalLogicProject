from Agent import Agent
import random

def randomInt ( limit ):
	return random.randrange(limit)

class MyAI ( Agent ):

    def __init__ ( self ):
        self.__moves = 0
        self.__safe_tiles = []
        self.__unsafe_tiles = set()
        self.__tile_history = []
        self.__x_tile = 1
        self.__y_tile = 1
        self.__dir = 'E'
        self.__move_history = []
        self.__has_gold = False
        self.__revert_home = False
        self.__path_home = []
        self.__dest_path = []
        self.__dest_node = (1,1)
        self.__xBorder = 0
        self.__yBorder = 0
        self.__in_danger = False
        self.__last_danger = (0,0)
        self.__x_border = 9
        self.__y_border = 9
        self.__stop_iteration = False
        self.__stopped_on_iteration = 0
        self.__dead_wump = False
        self.__found_wump = False
        self.__pitless_wump = False
        self.__wump_node = (0,0)
        self.__potential_wump_nodes = []
        self.__stench_nodes = []
        self.__potential_pit_nodes = []
        self.__breeze_nodes = []
        self.__shot_arrow = False
        self.__isInLoop = False
        pass

    def getAction( self, stench, breeze, glitter, bump, scream ):
        self.__check_bump(bump)
        self.__update_history_tiles()
        self.__moves+=1
        return self.__determineAction(stench, breeze, glitter, bump, scream)
    class Node:
        def __init__(self, x,y):
            self.__node = (x,y)
            self.__Nnode = (x,y+1)
            self.__Enode = (x+1,y)
            self.__Snode = (x,y-1)
            self.__Wnode = (x-1,y)
        def getCurrent(self):
            return self.__node
        def getNorth(self):
            return self.__Nnode
        def getEast(self):
            return self.__Enode
        def getSouth(self):
            return self.__Snode
        def getWest(self):
            return self.__Wnode
        def getX(self):
            return self.__node[0]
        def getY(self):
            return self.__node[1]
    def __getExploredAllSafeNodes(self):
         for i in range(len(self.__safe_tiles)):
            node = self.__safe_tiles[len(self.__safe_tiles)-i-1]
            if node not in self.__tile_history:
                return False
         return True

    def __Facing_Wump(self):
        if self.__dir == "N":
            if self.__wump_node[1]>self.__y_tile:
                return True
            else:
                return False
        elif self.__dir == "E":
            if self.__wump_node[0]>self.__x_tile:
                return True
            else:
                return False
        elif self.__dir == "S":
            if self.__wump_node[1]<self.__y_tile:
                return True
            else:
                return False
        elif self.__dir == "W":
            if self.__wump_node[0]<self.__x_tile:
                return True
            else:
                return False
        return True

    def __Align_To_Wump(self,stench, breeze, glitter, bump, scream):
        curNode = self.Node(self.__x_tile,self.__y_tile)
        nextNode = self.Node(self.__wump_node[0], self.__wump_node[1])
        self.__print_debug_info(stench, breeze, glitter, bump, scream)
        return self.__NodeToNode(nextNode,curNode)
        
    def __determineAction(self,stench, breeze, glitter, bump, scream ):
        print("Dest Node: (", self.__dest_node, ") current node: ", self.__x_tile, self.__y_tile)
        if scream:
            if self.__wump_node == (0,0):
                self.__wump_node = (2,1)
            self.__UpdateSafeStench()
            self.__dead_wump = True
            if self.__wump_node not in self.__safe_tiles:
                self.__safe_tiles.append(self.__wump_node)
            found_node = False
            for i in range(len(self.__safe_tiles)):
                node = self.__safe_tiles[len(self.__safe_tiles)-i-1]
                if node not in self.__tile_history:
                    self.__dest_node = (node[0], node[1])
                    self.__dest_path = self.__optimal_home_path(self.__x_tile,self.__y_tile,self.__dest_node[0],self.__dest_node[1])
                    self.__stop_iteration = False
                    found_node = True
                    break
            if not found_node:
                print('loop156')
                self.__revert_home = True
            else:
                self.__revert_home = False
        elif self.__moves == 2 and stench == True and self.__shot_arrow:
            self.__safe_tiles.append((2,1))
            self.__wump_node = (1,2)
            self.__potential_wump_nodes.append(self.__wump_node)
            self.__found_wump = True
            found_node = False
            for i in range(len(self.__safe_tiles)):
                node = self.__safe_tiles[len(self.__safe_tiles)-i-1]
                if node not in self.__tile_history:
                    self.__dest_node = (node[0], node[1])
                    self.__dest_path = self.__optimal_home_path(self.__x_tile,self.__y_tile,self.__dest_node[0],self.__dest_node[1])
                    self.__stop_iteration = False
                    found_node = True
                    break
            if not found_node:
                self.__revert_home = True
            else:
                self.__revert_home = False
        if self.__isInLoop == True: 
            print("**STILL IN LOOP**")
            gotnode = self.getloopbreakingnode(stench, breeze, glitter, bump, scream)
            return self.__go_to_dest(stench, breeze, glitter, bump, scream, gotnode[0], gotnode[1], False)
        if not breeze and not bump:
            if  not stench or (stench and self.__dead_wump):
                self.__UpdateSafeTileManual(self.__x_tile, self.__y_tile)
        if not self.__shot_arrow and self.__pitless_wump and not self.__dead_wump:
            if self.__Facing_Wump():
                self.__shot_arrow = True
                self.__print_debug_info(stench, breeze, glitter, bump, scream)
                return Agent.Action.SHOOT
            else:
                return self.__Align_To_Wump(stench, breeze, glitter, bump, scream)
        if breeze:
            self.__Update_Potential_Pit_Locations()
        if stench and not self.__found_wump:
            self.__Update_Potential_Wump_Locations()
        if (breeze or bump or (stench and not self.__dead_wump)):
            if bump:
                if self.__dir == 'E':
                    self.__x_border = self.__x_tile
                    for i in self.__safe_tiles:
                        if i[0] > self.__x_border:
                            self.__safe_tiles.remove(i)
                elif self.__dir == 'N':
                    self.__y_border = self.__y_tile
                    for i in self.__safe_tiles:
                        if i[1] > self.__y_border:
                            self.__safe_tiles.remove(i)

            if (not self.__in_danger) or (self.__in_danger and (self.__last_danger != (self.__x_tile,self.__y_tile)) or self.__dest_node not in self.__safe_tiles):
                found_node = False
                for i in range(len(self.__safe_tiles)):
                    node = self.__safe_tiles[len(self.__safe_tiles)-i-1]
                    if node not in self.__tile_history:
                        self.__dest_node = (node[0], node[1])
                        self.__dest_path = self.__optimal_home_path(self.__x_tile,self.__y_tile,self.__dest_node[0],self.__dest_node[1])
                        self.__stop_iteration = False
                        found_node = True
                        break
                self.__in_danger = True
                self.__last_danger = (self.__x_tile,self.__y_tile)
                if not found_node:
                    print('loop217')
                    self.__revert_home = True
        else:
            self.__in_danger = False
        if not self.__revert_home:
            if self.__moves > 1:
                if self.__getExploredAllSafeNodes():
                    print('loop225')
                    self.__revert_home = True
        if glitter == True: #Glitter Check
            self.__has_gold = True
            self.__revert_home = True
            self.__move_history.append("GRAB")
            self.__print_debug_info(stench, breeze, glitter, bump, scream)
            return Agent.Action.GRAB
        elif self.__has_gold == True and self.__x_tile == 1 and self.__y_tile == 1: #ClimbToWin
            self.__move_history.append("CLIMB")
            return Agent.Action.CLIMB
        elif self.__moves == 1 and breeze == True: #FirstMoveCheck
            curNode = self.Node(self.__x_tile,self.__y_tile)
            nextNode = self.Node(2, 1)
            return self.__NodeToNode(nextNode,curNode)
        elif self.__moves == 1 and stench == True:
            self.__shot_arrow = True
            self.__print_debug_info(stench, breeze, glitter, bump, scream)
            return Agent.Action.SHOOT

        elif self.__revert_home == True:
            print("**********Revert HOME********")
            if not self.__has_gold:
                self.__isInLoop = True
                print("isinloop turned True")
                self.__revert_home = False
                gotnode = self.getloopbreakingnode(stench, breeze, glitter, bump, scream)
                self.__dest_node = (gotnode[0], gotnode[1])
                return self.__go_to_dest(stench, breeze, glitter, bump, scream, gotnode[0], gotnode[1], True)

            else:
                destination = (1,1)
                return self.__go_to_dest( stench, breeze, glitter, bump, scream, 1,1, True)


        if self.__dest_node[0] == self.__x_tile and self.__dest_node[1] == self.__y_tile:
            self.__dest_node = (self.__dest_node[0] + (self.__dir_to_coordinate(self.__dir)[0]),
                                self.__dest_node[1] + (self.__dir_to_coordinate(self.__dir)[1]))
            curNode = self.Node(self.__x_tile,self.__y_tile)
            nextNode = self.Node(self.__dest_node[0], self.__dest_node[1])
            self.__print_debug_info(stench, breeze, glitter, bump, scream)
            return self.__NodeToNode(nextNode,curNode)
        else:
            curNode = self.Node(self.__x_tile,self.__y_tile)
            for i in range(len(self.__dest_path)):
                if self.__dest_path[i] == curNode.getCurrent():
                    index = i
                    break
            nextNode = self.Node(self.__dest_path[index+1][0],self.__dest_path[index+1][1])
            self.__print_debug_info(stench, breeze, glitter, bump, scream)
            return self.__NodeToNode(nextNode,curNode)


    def __go_to_dest(self,stench, breeze, glitter, bump, scream, destx, desty, first_time):
        if (first_time == True):
            self.__dest_node = (destx, desty)
        if len(self.__path_home) == 0:
            self.__path_home = self.__optimal_home_path(self.__x_tile,self.__y_tile,self.__dest_node[0],self.__dest_node[1])
            self.__stop_iteration = False
        elif self.__x_tile == 1 and self.__y_tile == 1 and self.__revert_home == True:
            self.__move_history.append("CLIMB")
            return Agent.Action.CLIMB
        elif self.__x_tile == self.__dest_node[0] and self.__y_tile == self.__dest_node[1] and self.__isInLoop == True:
            print("reached destination ", self.__dest_node[0], self.__dest_node[1], " inloop" )
            self.__isInLoop = False
            self.__dest_node = (self.__dest_node[0] + (self.__dir_to_coordinate(self.__dir)[0]),
                                self.__dest_node[1] + (self.__dir_to_coordinate(self.__dir)[1]))
            curNode = self.Node(self.__x_tile,self.__y_tile)
            nextNode = self.Node(self.__dest_node[0], self.__dest_node[1])
            self.__print_debug_info(stench, breeze, glitter, bump, scream)
            self.__safe_tiles.append(self.__dest_node)
            return self.__NodeToNode(nextNode,curNode)
        curNode = self.Node(self.__x_tile,self.__y_tile)
        index = 0
        for i in range(len(self.__path_home)):
            if self.__path_home[i] == curNode.getCurrent():
                index = i
                break
        try:
            nextNode = self.Node(self.__path_home[i+1][0],self.__path_home[i+1][1])
        except:
            self.__path_home = self.__optimal_home_path(self.__x_tile,self.__y_tile,self.__dest_node[0],self.__dest_node[1])
            self.__stop_iteration = False
            curNode = self.Node(self.__x_tile,self.__y_tile)
            if(len(self.__path_home)>1):
                index = 0
                for i in range(len(self.__path_home)):
                    if self.__path_home[i] == curNode.getCurrent():
                        index = i
                        break
                nextNode = self.Node(self.__path_home[i+1][0],self.__path_home[i+1][1])
            else: 
                self.__dest_node = (destx + (self.__dir_to_coordinate(self.__dir)[0]),
                                desty + (self.__dir_to_coordinate(self.__dir)[1]))
                curNode = self.Node(self.__x_tile,self.__y_tile)
                nextNode = self.Node(self.__dest_node[0], self.__dest_node[1])
                

        self.__print_debug_info(stench, breeze, glitter, bump, scream)
        return self.__NodeToNode(nextNode,curNode)

    def getloopbreakingnode(self,stench, breeze, glitter, bump, scream):
        possiblenodes = []
        for i in range(len(self.__tile_history)):
            nodetile = self.__tile_history[len(self.__tile_history)-i-1]
            gnode = self.Node(nodetile[0],nodetile[1])
            sidenode = gnode.getWest()

            if sidenode[0]>=1 and sidenode not in self.__tile_history and sidenode not in possiblenodes: #Left
                possiblenodes.append(sidenode)
            sidenode = gnode.getEast()
            if sidenode[0]<=self.__x_border and sidenode not in self.__tile_history and sidenode not in possiblenodes: #Right
                possiblenodes.append(sidenode)
            sidenode = gnode.getSouth()
            if sidenode[1]>=1 and sidenode not in self.__tile_history and sidenode not in possiblenodes: #down
                possiblenodes.append(sidenode)
            sidenode = gnode.getNorth()
            if sidenode[1]<=self.__y_border and sidenode not in self.__tile_history and sidenode not in possiblenodes: #Left
                possiblenodes.append(sidenode)
        size = len(possiblenodes)
        rand = randomInt(size)
        risk = 100000
        index = 0
        for i in range(len(possiblenodes)):
            sidenode = self.Node(possiblenodes[i][0], possiblenodes[i][1])
            temp = self.getbestpos(sidenode)
            print("temp risk : " , temp, sidenode.getCurrent())
            if(temp<risk):
                risk = temp
                index = i
        
        return possiblenodes[index]
            
    def getbestpos(self, gnode):
        risk = 0
        sidenode = gnode.getEast()
        if sidenode[0]<=self.__x_border:  #Right
            risk += self.calcRisk(sidenode)
            print("right")
        sidenode = gnode.getNorth()
        if sidenode[1]<=self.__y_border:
            risk+=self.calcRisk(sidenode)
            print("up")
        sidenode = gnode.getSouth()
        if sidenode[1]>=1:
            risk+=self.calcRisk(sidenode)
            print("down")
        sidenode = gnode.getWest()
        if sidenode[0]>=1:
            risk+=self.calcRisk(sidenode)
            print("left")
        return risk
        
    def calcRisk(self, sidenode):
        risk = 0
        if sidenode in self.__breeze_nodes:
            risk += 300
        if sidenode in self.__stench_nodes:
            risk += 300
        if sidenode in self.__safe_tiles:
            risk -=10
        return risk
            

    def __Update_Potential_Pit_Locations(self):
        if (self.__x_tile,self.__y_tile) in self.__breeze_nodes:
            return
        else:
            self.__breeze_nodes.append((self.__x_tile,self.__y_tile))
        Pit_Spots = []
        if self.__x_tile-1>=1: #Left
            if (self.__x_tile-1,self.__y_tile) not in self.__safe_tiles:
                Pit_Spots.append((self.__x_tile-1,self.__y_tile))
        if self.__x_tile+1<=self.__x_border: #Right
            if (self.__x_tile+1,self.__y_tile) not in self.__safe_tiles:
                Pit_Spots.append((self.__x_tile+1,self.__y_tile))
        if self.__y_tile-1>=1: #Down
            if (self.__x_tile,self.__y_tile-1) not in self.__safe_tiles:
                Pit_Spots.append((self.__x_tile,self.__y_tile-1))
        if self.__y_tile+1<=self.__y_border: #Up
            if (self.__x_tile,self.__y_tile+1) not in self.__safe_tiles:
                Pit_Spots.append((self.__x_tile,self.__y_tile+1))
        if len(Pit_Spots)==1:
            if Pit_Spots[0] not in self.__potential_pit_nodes:
                self.__potential_pit_nodes.append(Pit_Spots[0])
            return
        for node in Pit_Spots:
            if node not in self.__potential_pit_nodes:
                self.__potential_pit_nodes.append(node)
        
    def __Update_Potential_Wump_Locations(self):
        if (self.__x_tile,self.__y_tile) in self.__stench_nodes:
            return
        else:
            self.__stench_nodes.append((self.__x_tile,self.__y_tile))
        Wump_Spots = []
        if not self.__found_wump:
            if self.__x_tile-1>=1: #Left
                if (self.__x_tile-1,self.__y_tile) not in self.__safe_tiles:
                    Wump_Spots.append((self.__x_tile-1,self.__y_tile))
            if self.__x_tile+1<=self.__x_border: #Right
                if (self.__x_tile+1,self.__y_tile) not in self.__safe_tiles:
                    Wump_Spots.append((self.__x_tile+1,self.__y_tile))
            if self.__y_tile-1>=1: #Down
                if (self.__x_tile,self.__y_tile-1) not in self.__safe_tiles:
                    Wump_Spots.append((self.__x_tile,self.__y_tile-1))
            if self.__y_tile+1<=self.__y_border: #Up
                if (self.__x_tile,self.__y_tile+1) not in self.__safe_tiles:
                    Wump_Spots.append((self.__x_tile,self.__y_tile+1))
        if len(Wump_Spots)==1:
            self.__found_wump = True
            self.__potential_wump_nodes = []
            self.__potential_wump_nodes.append(Wump_Spots[0])
            self.__wump_node = Wump_Spots[0]
            return
        for node in Wump_Spots:
            if node in self.__potential_wump_nodes:
                self.__found_wump = True
                self.__potential_wump_nodes = []
                self.__potential_wump_nodes.append(node)
                self.__wump_node = node
                break
            else:
                self.__potential_wump_nodes.append(node)
                
        for node in self.__stench_nodes:
            if(self.stench_wump_check(node) == True):
                self.__found_wump = True
                break
        if self.__found_wump and not self.__pitless_wump:
            self.__pitless_wump = True

    def stench_wump_check(self, node):

        x = node[0]
        y = node[1]
        if (x-1>=1 and y+1<=self.__y_border): #leftup
            leftup = (x-1,y+1)
            if leftup in self.__stench_nodes: 
                if((x-1, y) in self.__safe_tiles):
                    self.__wump_node = (x,y+1)
                    return True
                elif((x, y+1) in self.__safe_tiles):
                    self.__wump_node = (x-1,y)
                    return True
        if (x-1>=1 and y-1>=1): #leftdown
            leftdown = (x-1,y-1)
            if leftdown in self.__stench_nodes: 
                if((x-1, y) in self.__safe_tiles):
                    self.__wump_node = (x,y-1)
                    return True
                elif((x, y-1) in self.__safe_tiles):
                    self.__wump_node = (x-1,y)
                    return True
        if (x+1<=self.__x_border and y+1<=self.__y_border): #rightup
            rightup = (x+1,y+1)
            if rightup in self.__stench_nodes: 
                if((x+1, y) in self.__safe_tiles):
                    self.__wump_node = (x,y+1)
                    return True
                elif((x, y+1) in self.__safe_tiles):
                    self.__wump_node = (x+1,y)
                    return True
        if (x+1<=self.__x_border and y-1>=1): #rightdown
            rightdown = (x+1,y-1)
            if rightdown in self.__stench_nodes: 
                if((x+1, y) in self.__safe_tiles):
                    self.__wump_node = (x,y-1)
                    return True
                elif((x, y-1) in self.__safe_tiles):
                    self.__wump_node = (x+1,y)
                    return True
        
        return False
    def __UpdateSafeStench(self):
        for node in self.__stench_nodes:
            if node not in self.__breeze_nodes:
                self.__UpdateSafeTileManual(node[0],node[1])
        
    def __UpdateSafeTileManual(self,x_tile,y_tile):        
        if (x_tile,y_tile) not in self.__safe_tiles:
            self.__safe_tiles.append((x_tile,y_tile))
            if (x_tile,y_tile) in self.__potential_wump_nodes:
                self.__potential_wump_nodes.remove((x_tile,y_tile))
            if (x_tile,y_tile) in self.__potential_pit_nodes:
                self.__potential_pit_nodes.remove((x_tile,y_tile))
        if x_tile-1>=1: #Left
            if (x_tile-1,y_tile) not in self.__safe_tiles:
                self.__safe_tiles.append((x_tile-1,y_tile))
                if (x_tile-1,y_tile) in self.__potential_wump_nodes:
                    self.__potential_wump_nodes.remove((x_tile-1,y_tile))
                if (x_tile-1,y_tile) in self.__potential_pit_nodes:
                    self.__potential_pit_nodes.remove((x_tile-1,y_tile))
        if x_tile+1<=self.__x_border: #Right
            if (x_tile+1,y_tile) not in self.__safe_tiles:
                self.__safe_tiles.append((x_tile+1,y_tile))
                if (x_tile+1,y_tile) in self.__potential_wump_nodes:
                    self.__potential_wump_nodes.remove((x_tile+1,y_tile))
                if (x_tile+1,y_tile) in self.__potential_pit_nodes:
                    self.__potential_pit_nodes.remove((x_tile+1,y_tile))
        if y_tile-1>=1: #Down
            if (x_tile,y_tile-1) not in self.__safe_tiles:
                self.__safe_tiles.append((x_tile,y_tile-1))
                if (x_tile,y_tile-1) in self.__potential_wump_nodes:
                    self.__potential_wump_nodes.remove((x_tile,y_tile-1))
                if (x_tile,y_tile-1) in self.__potential_pit_nodes:
                    self.__potential_pit_nodes.remove((x_tile,y_tile-1))
        if y_tile+1<=self.__y_border: #Up
            if (x_tile,y_tile+1) not in self.__safe_tiles:
                self.__safe_tiles.append((x_tile,y_tile+1))
                if (x_tile,y_tile+1) in self.__potential_wump_nodes:
                    self.__potential_wump_nodes.remove((x_tile,y_tile+1))
                if (x_tile,y_tile+1) in self.__potential_pit_nodes:
                    self.__potential_pit_nodes.remove((x_tile,y_tile+1))

    def __NodeToNode(self, potentialNode, CurrentNode):
        xValue = potentialNode.getX() - CurrentNode.getX()
        yValue = potentialNode.getY() - CurrentNode.getY()
        if (xValue,yValue) == (0,1):
            return self.__GoNorth()
        elif (xValue,yValue) == (1,0):
            return self.__GoEast()
        elif (xValue,yValue) == (0,-1):
            return self.__GoSouth()
        elif (xValue,yValue) == (-1,0):
            return self.__GoWest()
        else:
            return self.__GoNorth()

    def __GoNorth(self):
        if self.__dir == 'N':#N
            self.__move_history.append("FORWARD")
            self.__x_tile += self.__dir_to_coordinate(self.__dir)[0]
            self.__y_tile += self.__dir_to_coordinate(self.__dir)[1]
            return Agent.Action.FORWARD
        elif self.__dir == 'E':#E
            self.__dir = 'N'
            self.__move_history.append("LEFT")
            return Agent.Action.TURN_LEFT
        elif self.__dir == 'S':#S
            self.__dir = 'E'
            self.__move_history.append("LEFT")
            return Agent.Action.TURN_LEFT
        elif self.__dir == 'W':#W
            self.__dir = 'N'
            self.__move_history.append("RIGHT")
            return Agent.Action.TURN_RIGHT
    def __GoEast(self):
        if self.__dir == 'N':#N
            self.__dir = 'E'
            self.__move_history.append("RIGHT")
            return Agent.Action.TURN_RIGHT
        elif self.__dir == 'E':#E
            self.__move_history.append("FORWARD")
            self.__x_tile += self.__dir_to_coordinate(self.__dir)[0]
            self.__y_tile += self.__dir_to_coordinate(self.__dir)[1]
            return Agent.Action.FORWARD
        elif self.__dir == 'S':#S
            self.__dir = 'E'
            self.__move_history.append("LEFT")
            return Agent.Action.TURN_LEFT
        elif self.__dir == 'W':#W
            self.__dir = 'S'
            self.__move_history.append("LEFT")
            return Agent.Action.TURN_LEFT
    def __GoSouth(self):
        if self.__dir == 'N':
            self.__dir = 'W'
            self.__move_history.append("LEFT")
            return Agent.Action.TURN_LEFT
        elif self.__dir == 'E':
            self.__dir = 'S'
            self.__move_history.append("RIGHT")
            return Agent.Action.TURN_RIGHT
        elif self.__dir == 'S':
            self.__move_history.append("FORWARD")
            self.__x_tile += self.__dir_to_coordinate(self.__dir)[0]
            self.__y_tile += self.__dir_to_coordinate(self.__dir)[1]
            return Agent.Action.FORWARD
        elif self.__dir == 'W':
            self.__dir = 'S'
            self.__move_history.append("LEFT")
            return Agent.Action.TURN_LEFT
    def __GoWest(self):
        if self.__dir == 'N':
            self.__dir = 'W'
            self.__move_history.append("LEFT")
            return Agent.Action.TURN_LEFT
        elif self.__dir == 'E':
            self.__dir = 'N'
            self.__move_history.append("LEFT")
            return Agent.Action.TURN_LEFT
        elif self.__dir == 'S':
            self.__dir = 'W'
            self.__move_history.append("RIGHT")
            return Agent.Action.TURN_RIGHT
        elif self.__dir == 'W':
            self.__move_history.append("FORWARD")
            self.__x_tile += self.__dir_to_coordinate(self.__dir)[0]
            self.__y_tile += self.__dir_to_coordinate(self.__dir)[1]
            return Agent.Action.FORWARD
        
    def __optimal_home_path(self,x,y, x_target,y_target):
        '''Returns Optimal Path'''
        Path = self.__potential_path(x,y,[], x_target,y_target, 0)
        print("Path to (", x_target, y_target, "): ")
        print(Path)
        if Path[-1][0] != x_target or Path[-1][1] != y_target:
            self.__dest_node = (Path[-1][0],Path[-1][1])
        return Path
            
    def __potential_path(self,x,y,memory,x_target,y_target, iteration):
        node = self.Node(x,y)
        explored = []
        explored.extend(memory)
        if self.__stop_iteration == True:
            if iteration >= self.__stopped_on_iteration:
                return explored
        if node.getCurrent() == (x_target,y_target):
            explored.append(node.getCurrent())
            self.__stop_iteration = True
            self.__stopped_on_iteration = iteration
            return explored
        elif node.getCurrent() not in self.__safe_tiles:
            explored.append(node.getCurrent())
            return explored
        elif node.getCurrent() in explored:
            return explored
        elif iteration >= 15:
            return explored
        else:
            explored.append(node.getCurrent())
            NNodes = self.__potential_path(node.getNorth()[0],node.getNorth()[1],explored,x_target,y_target,iteration+1)
            ENodes = self.__potential_path(node.getEast()[0],node.getEast()[1],explored,x_target,y_target,iteration+1)
            SNodes = self.__potential_path(node.getSouth()[0],node.getSouth()[1],explored,x_target,y_target,iteration+1)
            WNodes = self.__potential_path(node.getWest()[0],node.getWest()[1],explored,x_target,y_target,iteration+1)
            Paths = [NNodes, ENodes, SNodes, WNodes]
            null_paths = []
            for i in range(len(Paths)):
                if len(Paths[i]) != 0 and Paths[i][-1] != (x_target,y_target):
                    null_paths.append(i)
            null_close = False
            if len(null_paths) != 4:
               for i in null_paths:
                   Paths[i].clear()
            else:
                null_close = True
            
            if null_close:
                best_node = (99,99)
                ind = 0
                for i in range(len(Paths)):
                    if len(Paths[i]) != 0:
                        if self.__NodeDifference(Paths[i][-1][0],Paths[i][-1][1],x_target,y_target) < self.__NodeDifference(best_node[0],best_node[1],x_target,y_target):
                            best_node = (Paths[i][-1][0],Paths[i][-1][1])
                            ind = i
                for i in range(len(Paths)):
                    if i!=ind:
                        Paths[i].clear()
            BestPath = []    
            for i in range(len(Paths)):
                if len(Paths[i]) != 0:
                    if len(BestPath) == 0:
                        BestPath = Paths[i]
                    elif len(Paths[i]) < len(BestPath):
                        BestPath = Paths[i]
            return BestPath
                
    def __NodeDifference(self,x1,y1,x2,y2):
        x_score = x2-x1
        y_score = y2-y1

        if x_score<0:
            x_score = x_score*-1
        if y_score<0:
            y_score = y_score*-1
        node_score = x_score+y_score
        return node_score
        
    def __dir_to_coordinate(self, direction):
        if direction == 'N':
            return (0,1)
        elif direction == 'E':
            return (1,0)
        elif direction == 'S':
            return (0,-1)
        elif direction == 'W':
            return (-1,0)
        else:
            return (0,1)

    def __check_bump(self,bump):
        if(bump==True):
           self.__x_tile -= self.__dir_to_coordinate(self.__dir)[0]
           self.__y_tile -= self.__dir_to_coordinate(self.__dir)[1]
           if self.__dir == 'N':
               self.__yBorder = self.__y_tile
           elif self.__dir == 'E':
               self.__xBorder = self.__x_tile

    def __update_history_tiles(self):
        if len(self.__tile_history) == 0:
            self.__tile_history.append((self.__x_tile,self.__y_tile))
        elif self.__tile_history[-1]!=(self.__x_tile,self.__y_tile):
            self.__tile_history.append((self.__x_tile,self.__y_tile))
        if (self.__x_tile,self.__y_tile) not in self.__safe_tiles:
            self.__safe_tiles.append((self.__x_tile,self.__y_tile))

    def __print_debug_info(self, stench, breeze, glitter, bump, scream ):
        """
        print("\n---------Debug Info--------------------")
        print("DIRECTION: "+str(self.__dir))
        print("MOVES: "+str(self.__moves))
        print("SAFE TILES: "+str(self.__safe_tiles))
        print("HISTORY TILES: "+str(self.__tile_history))
        print("MOVE HISTORY: "+str(self.__move_history))
        print("COORDINATE: "+str((self.__x_tile,self.__y_tile)))
        print("STENCH: "+str(stench))
        print("BREEZE: "+str(breeze))
        print("GLITTER: "+str(glitter))
        print("BUMP: "+str(bump))
        print("SCREAM: "+str(scream))
        print("XBoarder: "+ str(self.__x_border))
        print("YBoarder: "+str(self.__y_border ))
        print("Path Home: "+str(self.__path_home))
        print("Destination Path: "+str(self.__dest_path ))
        print("Destination Node: "+str(self.__dest_node))
        print("Found Wumpus: "+str(self.__found_wump))
        print("Potential Wump Nodes: "+str(self.__potential_wump_nodes))
        print("Stench Nodes: "+str(self.__stench_nodes))
        print("Potential Pit Nodes: "+str(self.__potential_pit_nodes))
        print("Breeze Nodes: "+str(self.__breeze_nodes))
        print("Pitless Wump: "+str(self.__pitless_wump))
        print("---------------------------------------\n")
        """
        pass
