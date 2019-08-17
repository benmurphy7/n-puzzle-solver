import sys
import copy
import heapq
from collections import deque

start = []
tried = {} #used to keep track of tried moves and their preceding (parent) move
next_m = deque() #queue for next moves
test_m = deque()
steps = deque()
cost = deque()
h = []
sol_found = False
abort = False
solution = []
expanded = 0
frontier = 1
explored = 0
max_size = 0
def getPuzzle():
    path = ''
    for x in range (1, len(sys.argv)): #collect full path (including possible spaces)
        path = path + sys.argv[x] + ' '
    file = open(path, 'r')
    for line in file:
        start.append([str(s) for s in line.split()])
    file.close()
    tried[getString(start)] = "Root"
    heapq.heappush(h, [0,start])

def printState(s):
    for x in range (0, len(s)):
        print()
        for y in range(0, len(s)):
            print (s[x][y], end='')
            if len(s[x][y]) ==1:
                print("  ", end='')
            else:
                print(" ",end ='')

    print()

def solState(s): #saves the solved state of the puzzle for comparison
    sol = copy.deepcopy(s)
    val = 1
    for x in range(0, len(s)):
        for y in range(0, len(s)):
            if x == 0 and y == 0:
                sol[x][y] = '.'
            else:
                sol[x][y] = str(val)
                val+=1
    return sol

def findIn(s,v): #returns x,y
    location = [-50,-50]
    for x in range(0,len(s)):
        for y in range(0,len(s)):
            if str(v) == str(s[x][y]):
                location[0] = x
                location[1] = y
                return location
    return location
def calcDist(s): #calculates total Manhattan distance from current to solved state
    global solution
    dist = 0
    for x in range(0,len(s)):
        for y in range(0,len(s)):
            if not s[x][y] == '.':
                loc = (findIn(s,solution[x][y]))
                dist += abs(int(loc[0]-x)) + abs(int(loc[1]-y))
    return dist



def isSolved(s):
    if s[0][0] == '.':
        val = 1
        for x in range(0, len(s)):
            for y in range(0, len(s)):
                if x == 0 and y == 0:
                    pass
                elif s[x][y] != str(val):
                    return False
                else: val +=1

        return True
    return False

def valMoves(s_cost, state): #checks valid directions the empty space can move
    global frontier
    doty = -1
    dotx = -1
    valid_moves = ['L', 'R', 'U', 'D']
    move_states = []
    for x in range(0, len(state)):
        for y in range(0, len(state)):
            if state[x][y]== '.':
                doty = y
                dotx = x
    if doty == -1 or dotx == -1:
        print("\'.\' not found")

    if doty == 0:
        valid_moves.remove('L')
    elif doty == len(state)-1:
        valid_moves.remove('R')
    if dotx == 0:
        valid_moves.remove('U')
    elif dotx == len(state)-1:
        valid_moves.remove('D')

    for move in valid_moves: #changes state according to valid moves
        test = copy.deepcopy(state)
        if move == 'L':
            test[dotx][doty] = test[dotx][doty-1]
            test[dotx][doty - 1] = '.'
            move_states.append(test)

        elif move == 'R':
            test[dotx][doty] = test[dotx][doty + 1]
            test[dotx][doty + 1] = '.'
            move_states.append(test)

        elif move == 'U':
            test[dotx][doty] = test[dotx-1][doty]
            test[dotx-1][doty] = '.'
            move_states.append(test)

        elif move == 'D':
            test[dotx][doty] = test[dotx+1][doty]
            test[dotx+1][doty] = '.'
            move_states.append(test)

    for s in move_states: #turns each move state into a string
        move_str = getString(s)
        if move_str not in tried: #adds new move to dictionary
            tried[move_str] = state #parent node
            heapq.heappush(h, [s_cost - calcDist(state) + 1 + calcDist(s),s])
            #cost function (s_cost - calcDist(state) + 1 is the number of moves made so far)
            frontier += 1

def getString(s): #returns state as string
    list = sum(s, [])
    str = ''.join(list)
    return str

def showSteps(s):
    move_str = getString(s)
    while not tried.get(move_str)=="Root":
        steps.append(tried.get(move_str))
        move_str = getString(tried.get(move_str))
    print("\nSolution moves: " + str(len(steps)))
    while not len(steps)==0:
        printState(steps[len(steps)-1])
        steps.pop()
    printState(solution)

getPuzzle()
solution = solState(start) #sets solution state for comparison
while sol_found == False and abort==False:
    while not len(h) == 0:
        if len(h) > max_size:
            max_size = len(h)
        best = heapq.heappop(h)
        explored+=1
        if isSolved(best[1]):
            sol_found = True
            solution = copy.deepcopy(best[1])
            break
        expanded+=1
        valMoves(best[0],best[1])
        if explored>= 100000:
            print("no solution found (100k limit reached)")
            abort = True
            break
    if sol_found:
        break

print("\nTotal added to frontier queue: " + str(frontier))
print("Selected for expansion: " + str(expanded))
print("Max size of search queue: " + str(max_size))


if not abort:
    showSteps(solution)

