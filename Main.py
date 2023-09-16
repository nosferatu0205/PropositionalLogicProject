
from Agent import *
import itertools
import copy



total_count=0

kb=[]


actions = []

#current_status = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
current_status = [[0 for _ in range(10)] for _ in range(10)]
allowed_moves = [[0,1],[0,-1],[1,0],[-1,0]]                     
moves = ['Up','Down','Right','Left']
moves_taken = []

def FindAdjacentRooms(cl):
    cLoc = cl
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

def legal(r,c):
    if(r>=0 and r<10 and c>=0 and c<10):
        return True
    else:
        return False


def bfs(current,target):
    visited = []
    for i in range(10):
        visited.append([False]*10)
    q = []
    dir = {(current[0],current[1]):(None,None)}
    q.append((current[0],current[1]))
    visited[current[0]][current[1]]=True                    
    while q:
        s = q.pop(0)

        if s[0]==target[0] and s[1]==target[1]:
            break
        for i in range(4):
            newr = s[0]+allowed_moves[i][0]
            newc = s[1]+allowed_moves[i][1]
            if legal(newr,newc) and visited[newr][newc]==False:
                visited[newr][newc]=True
                q.append((newr,newc))
                dir[(newr,newc)]=((s[0],s[1]),moves[i])

    target_moves = []
    top = (target[0],target[1])
    while top!=(current[0],current[1]):

        target_moves.append(dir[top][1])
        top = dir[top][0]
    
    target_moves.reverse()
    return target_moves


def initialize(ag):
    big_s1 = set()  
    big_s2 = set()
    for i in range(10):
        for j in range(10):
            for l, r in (('B', 'P'), ('S', 'W')):
                neighbours = FindAdjacentRooms([i+1,j+1])
                first_element = set()
                for x,y in neighbours:
                    first_element.add((f'{r}{x}{y}',1))
                first_element.add((f'{l}{i+1}{j+1}',0))
                kb.append(first_element)
                for x,y in neighbours:
                    kb.append({(f'{r}{x}{y}',0),(f'{l}{i+1}{j+1}',1)})
                if(r=='P'):
                    big_s1.add((f'{r}{i+1}{j+1}',1))    
                else:
                    big_s2.add((f'{r}{i+1}{j+1}',1))

    kb.append(big_s1)
    kb.append(big_s2)

    k=0
    store = dict()
    for i in range(10):
        for j in range(10):
            for i1 in range(10):
                for j1 in range(10):
                    if i1==i and j1 ==j:
                        continue
                    else:
                        temp = set()
                        temp.add((f'W{i+1}{j+1}',0))
                        temp.add((f'W{i1+1}{j1+1}',0))
                        temp1 = ((f'W{i+1}{j+1}',0),(f'W{i1+1}{j1+1}',0))
                        temp2 = ((f'W{i1+1}{j1+1}',0),(f'W{i+1}{j+1}',0))
                        if (temp1 not in store) or (temp2 not in store):
                            store[temp1]=1
                            store[temp2]=1

                            k+=1
                            kb.append({(f'W{i+1}{j+1}',0),(f'W{i1+1}{j1+1}',0)})
                            kb.append({(f'P{i+1}{j+1}',0),(f'P{i1+1}{j1+1}',0)})
    

  

def literal_expr(expr):
    for c in expr:
        for d in c:
            return d[0]
 
"""
def dpll(expr):   
    global total_count
    total_count+=1       

    ps = pure_symbols(expr)

    expr_new = []
    to_add = True
    if len(ps)!=0:
        for c in expr:
            for k in c:
                if k in ps:
                    to_add = False
                    break
            if to_add==True:
                expr_new.append(c)
            to_add = True
    else:
        expr_new = copy.deepcopy(expr)



    polarity,uc = unit_clauses(expr_new)
    if polarity==False:

        return False

    if len(uc)!=0:

        for i in uc:

            expr_new.remove(i)

        to_change = []
        to_add = True
        for k in expr_new:
            for j in k:
                for i in uc:
                    for z in i:
                        if z==j:

                            to_add=False
                            break
                if to_add==False:
                    break
            if to_add==True:
                to_change.append(k)
            to_add=True


        
        for i in uc:
            new_one= None
            for k in i:
                new_one = {(k[0],1-k[1])}

            to_change = [c.difference(new_one) for c in to_change]

        
        expr_new= copy.deepcopy(to_change)
    

    if(len(expr_new)==0):

        return True

    if any([len(c)==0 for c in expr_new]):
        return False

    if(expr_new!=expr):

        return dpll(expr_new)
    else:
        cnf = copy.deepcopy(expr_new)
        l = literal_expr(cnf)
        expr_new_one=[]

        for c in cnf:
            if (l,1) not in c:
                expr_new_one.append(c)
        expr_new_one = [c.difference({(l, 0)}) for c in expr_new_one]
        done = dpll(expr_new_one)
        if done==True:
            return done

        expr_new_one = []

        for c in cnf:
            if (l,0) not in c:
                expr_new_one.append(c)
        expr_new_one = [c.difference({(l, 1)}) for c in expr_new_one]
        done = dpll(expr_new_one)
        if done==True:
            return done

        return False
    return None
"""

def dpll(expr):
    global total_count
    total_count += 1

    ps = pure_symbols(expr)

    if len(ps) != 0:
        expr_new = [c for c in expr if not any(k in ps for k in c)]
    else:
        expr_new = expr[:]

    polarity, uc = unit_clauses(expr_new)
    if not polarity:
        return False

    if len(uc) != 0:
        for i in uc:
            expr_new.remove(i)

        to_change = []
        for k in expr_new:
            to_add = True
            for j in k:
                for i in uc:
                    if any(z == j for z in i):
                        to_add = False
                        break
                if not to_add:
                    break
            if to_add:
                to_change.append(k)

        for i in uc:
            new_one = {(k[0], 1 - k[1]) for k in i}
            to_change = [c.difference(new_one) for c in to_change]

        expr_new = to_change[:]

    if not expr_new:
        return True

    if any(len(c) == 0 for c in expr_new):
        return False

    if expr_new != expr:
        return dpll(expr_new)
    else:
        cnf = expr_new[:]
        l = literal_expr(cnf)
        expr_new_one = [c for c in cnf if (l, 1) not in c]
        expr_new_one = [c.difference({(l, 0)}) for c in expr_new_one]
        done = dpll(expr_new_one)
        if done:
            return done

        expr_new_one = [c for c in cnf if (l, 0) not in c]
        expr_new_one = [c.difference({(l, 1)}) for c in expr_new_one]
        done = dpll(expr_new_one)
        if done:
            return done

        return False

    return None


def pure_symbols(expr):
    symbols = set()
    for c in expr:
        for d in c:
            symbols.add(d[0])

    main_list = dict()                      
    holding_val = dict()
    for i in symbols:
        main_list[i]=True
    
    for a in expr:
        for b in a:

            if main_list[b[0]]==False:
                continue
            if b[0] in holding_val:
                if b[1]!=holding_val[b[0]]:
                    main_list[b[0]]=False
            else:
                holding_val[b[0]]=b[1]

    to_ret = set()
    for i in main_list:
        if main_list[i]==True:
            to_ret.add((i,holding_val[i]))


    return to_ret

def unit_clauses(expr):
    to_ret = list()
    to_ret_cons = True
    track_truth = dict()
    for d in expr:
        if(len(d)==1):
            for t in d:
                to_ret.append({t})
                if t[0] not in track_truth:
                    track_truth[t[0]]=t[1]
                else:
                    if t[1]!=track_truth[t[0]]:
                        to_ret_cons=False
                        break

    return to_ret_cons,to_ret



def simulation(ag):

    stack = [[1,1]]
    current_status[0][0]=1
    visited = dict()
    visited[(0,0)]=1

    while(ag.FindCurrentLocation()!=[10,10]):
        my_tile = ag.FindCurrentLocation()
        stack.pop()
        visited[(my_tile[0],my_tile[1])]=1

        breeze,stench = ag.PerceiveCurrentLocation()
       
        if breeze == True:

            kb.append({(f'B{my_tile[0]}{my_tile[1]}',1)})
        else:

            kb.append({(f'B{my_tile[0]}{my_tile[1]}',0)})
        
        if stench == True:

            kb.append({(f'S{my_tile[0]}{my_tile[1]}',1)})
        else:

            kb.append({(f'S{my_tile[0]}{my_tile[1]}',0)})

        adj_rooms = FindAdjacentRooms([my_tile[0],my_tile[1]])

        for room in adj_rooms:
            if (room[0],room[1]) in visited:
                continue


            wump_alive = {(f'W{room[0]}{room[1]}',1)}
            kb.append(wump_alive)
            val1 = dpll(kb)
            if val1 == True :

                kb.remove(wump_alive)
                wump_alive_here = {(f'W{room[0]}{room[1]}',0)}
                kb.append(wump_alive_here)
                val11 = dpll(kb)
                if(val11==False):
                    kb.remove(wump_alive_here)
                    kb.append(wump_alive)

                    current_status[room[0]-1][room[1]-1]=2
                else:
                    kb.remove(wump_alive_here)
                continue
            kb.remove(wump_alive)
            kb.append({(f'W{room[0]}{room[1]}',0)})
            pit_present = {(f'P{room[0]}{room[1]}',1)}
            kb.append(pit_present)
            val2 = dpll(kb)
            if val2 == True:

                kb.remove(pit_present)
                pit_present_here = {(f'P{room[0]}{room[1]}',0)}
                kb.append(pit_present_here)
                val21 = dpll(kb)
                if(val21==False):
                    kb.remove(pit_present_here)
                    kb.append(pit_present)

                    current_status[room[0]-1][room[1]-1]=2
                else:
                    kb.remove(pit_present_here)
                continue
            kb.remove(pit_present)
            kb.append({(f'P{room[0]}{room[1]}',0)})
            stack.append(room)
            current_status[room[0]-1][room[1]-1]=1
            


        new_location = []


        if len(stack)==0:
            stack.append([1,1])
            visited.clear()

        new_location = stack[-1] 
        p1 = [my_tile[0]-1,my_tile[1]-1]
        p2 = [new_location[0]-1,new_location[1]-1]
        path = bfs(p1,p2)

        for p in path:
            ag.TakeAction(p)
            actions.append(p)
            moves_taken.append(ag.FindCurrentLocation())

    print("tiles gone to reach: ",moves_taken)
    print("actions taken to reach: ",actions)
    print("total number of calls to dpll: ",total_count)
    return None

def main():
    ag = Agent()
    initialize(ag)
    print("Generated Wumpus World:")
    for row in ag._wumpusWorld:
        print(" ".join(row))
    simulation(ag)



if __name__=='__main__':
    main()