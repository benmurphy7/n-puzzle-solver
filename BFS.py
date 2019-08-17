import sys
import copy
from collections import deque

start = []
tried = {} #used to keep track of tried moves and their preceding (parent) move
next_m = deque() #queue for next moves
test_m = deque()
steps = deque()
sol_found = False
abort = False
solution = []
expanded = 0
frontier = 0
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
    next_m.append(start)

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

def valMoves(state): #checks valid directions the empty space can move
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
            next_m.append(s)

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
while sol_found == False and abort==False:
    frontier += len(next_m)
    while not len(next_m)==0 and abort == False:
        test_m.append(next_m[0])
        next_m.popleft()
    if len(test_m) > max_size:
        max_size = len(test_m)
    for x in range (0,len(test_m)):
        explored +=1
        if(isSolved(test_m[x])):
            sol_found = True
            solution = copy.deepcopy(test_m[x])
            break
        if explored>= 100000:
            print("no solution found (100k limit reached)")
            abort = True
            break
    if sol_found:
        break
    while not len(test_m)==0:
        valMoves(test_m[0])
        test_m.popleft()
        expanded +=1

print("\nTotal added to frontier queue: " + str(frontier))
print("Selected for expansion: " + str(expanded))
print("Max size of search queue: " + str(max_size))

if not abort:
    showSteps(solution)




"""printState(start)
print(isSolved(start))
print(str(valMoves(start)))
print(str(valMoves(start)))
print("Valid Moves: " + str(valMoves(start)))"""

