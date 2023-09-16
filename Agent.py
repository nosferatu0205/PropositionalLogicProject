
class Agent:
    def __init__(self):
        self._wumpusWorld = [
                 ['','','','','','','','','',''],
                 ['','W','P','','','','','','',''],
                 ['','','','','','P','','','',''],
                 ['', '', 'P', '', '', '', '', '', 'P', ''],
                 ['', '', 'P', '', '', '', '', '', 'P', ''],
                 ['', '', '', '', 'P', '', '', '', '', ''],
                 ['', '', '', '', '', '', '', '', '', ''],
                 ['', '', '', 'P', '', '', '', '', '', ''],
                 ['', '', '', '', '', 'P', '', '', 'P', ''],
                 ['', 'P', '', '', '', 'P', '', '', '', ''],
                ]
        self._curLoc = [1,1]
        self._isAlive = True
        self._hasExited = False

    def _FindIndicesForLocation(self,loc):
        x,y = loc
        i,j = y-1, x-1
        return i,j

    def _CheckForPitWumpus(self):
        ww = self._wumpusWorld
        i,j = self._FindIndicesForLocation(self._curLoc)
        if 'P' in ww[i][j] or 'W' in ww[i][j]:
            print(ww[i][j])
            self._isAlive = False
            print('Agent is DEAD.')
        return self._isAlive

    def TakeAction(self,action):
        validActions = ['Up','Down','Left','Right']
        assert action in validActions, 'Invalid Action.'
        if self._isAlive == False:
            print('Action cannot be performed. Agent is DEAD. Location:{0}'.format(self._curLoc))
            return False
        if self._hasExited == True:
            print('Action cannot be performed. Agent has exited the Wumpus world.'.format(self._curLoc))
            return False

        index = validActions.index(action)
        validMoves = [[0,1],[0,-1],[-1,0],[1,0]]
        move = validMoves[index]
        newLoc = []
        for v, inc in zip(self._curLoc,move):
            z = v + inc
            z = 10 if z>10 else 1 if z<1 else z
            newLoc.append(z)
        self._curLoc = newLoc
        print('Action Taken: {0}, Current Location {1}'.format(action,self._curLoc))
        if self._curLoc[0]==10 and self._curLoc[1]==10:
            self._hasExited=True
        return self._CheckForPitWumpus()
    
    def _FindAdjacentRooms(self):
        cLoc = self._curLoc
        validMoves = [[0,1],[0,-1],[-1,0],[1,0]]
        adjRooms = []
        for vM in validMoves:
            room = []
            valid = True
            for v, inc in zip(cLoc,vM):
                z = v + inc
                if z<1 or z>10:
                    valid = False
                    break
                else:
                    room.append(z)
            if valid==True:
                adjRooms.append(room)
        return adjRooms
                
        
    def PerceiveCurrentLocation(self):
        breeze, stench = False, False
        ww = self._wumpusWorld
        if self._isAlive == False:
            print('Agent cannot perceive. Agent is DEAD. Location:{0}'.format(self._curLoc))
            return [None,None]
        if self._hasExited == True:
            print('Agent cannot perceive. Agent has exited the Wumpus World.'.format(self._curLoc))
            return [None,None]

        adjRooms = self._FindAdjacentRooms()
        for room in adjRooms:
            i,j = self._FindIndicesForLocation(room)
            if 'P' in ww[i][j]:
                breeze = True
            if 'W' in ww[i][j]:
                stench = True
        return [breeze,stench]
    
    def FindCurrentLocation(self):
        return self._curLoc
