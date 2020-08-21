import random
import time
from collections import deque
final_state = '12345670'
grid_size = 2
do = ['up', 'down', 'left', 'right', 'forward', 'back']
possible_moves = {0:['forward', 'right', 'down'], 1:['down', 'left', 'forward'], 2:['down', 'right', 'back'], 3:['left', 'down', 'back'], 4:['up', 'forward', 'right'], 5:['up','forward', 'left'], 6:['up', 'right', 'back'], 7:['up', 'left', 'back']}
visited_states = set()
def main():

    #print("A possible solvable puzzle: " + make_puzzle(Node()))
    print('Number of states possible: ' + str(bfspossible()))
    listofpuzzles = randpuzzle(3)
    for puzzle in listofpuzzles:
        print('PUZZLE: ' + puzzle)
        solved_node = bfssolve(Node(puzzle, None))
        result = 'LENGTH: ' + str(path(solved_node))
        print('Solved Puzzle: ' + solved_node.state + '\t' + result)

    '''
    string = input("Input a 9char solvable puzzle: ")
    tic = time.time()
    solved_node = bfssolve(Node(string, None))
    toc = time.time()
    print(toc - tic)
    result = 'LENGTH: ' + str(path(solved_node))
    print('PUZZLE: ' + string + '\t' + result)
    '''
    '''
    file = open('puzzle.txt', 'r')
    tic = time.time()
    for line in file.read().splitlines():
        a = bfssolve(Node(line, None))
        print('PUZZLE: ' + line + '\t' + 'LENGTH: ' + str(path(a)))
        visited_states.clear()
    toc = time.time()
    print(toc-tic)
    '''

def randpuzzle(times):
    return random.sample(visited_states, times)

def bfssolve(state):
    visited_states.clear()
    visited_states.add(state.state)
    fringe = deque()
    fringe.append(state)
    while fringe:
        v = fringe.popleft()
        if v.state == final_state:
            return v
        for d in possible_moves[v.state.find('0')]:
            temp = make_move(v.state, d)
            if temp not in visited_states:
                child = Node(temp, v)
                if not (child.state in visited_states or child.state is None):
                    v.children.append(child)
                    visited_states.add(child.state)
                    fringe.append(child)
    return None
def bfspossible():
    visited_states.clear()
    visited_states.add(final_state)
    count = 1
    fringe = deque()
    fringe.append(Node())
    while fringe:
        v = fringe.popleft()
        for d in possible_moves[v.state.find('0')]:
            temp = make_move(v.state, d)
            if temp not in visited_states:
                child = Node(temp, v)
                count += 1
                visited_states.add(child.state)
                fringe.append(child)
    return count



def path(state):
    if state is None:
        return 0
    elif state.parent is None:
        return 1
    else:
        count = 1 + path(state.parent)
        return count

def make_puzzle(grid):
    a = random.randint(20, 100)
    for x in range(a):
        temp = make_move(grid.state, random.choice(do))
        if temp is not None:
            grid.state = temp
    return grid.state


def swap(state, zi, zj, zk, di, dj, dk):
    value = get_ij(state, di, dj, dk)
    zeroindex = zi + grid_size * zj + grid_size**2*zk
    dindex = di + grid_size * dj + grid_size*2*dk
    if zeroindex < dindex:
        return state[:zeroindex] + value + state[zeroindex + 1 : dindex] + '0' + state[dindex+1:]
    else:
        return state[:dindex] + '0' + state[dindex + 1: zeroindex] + value + state[zeroindex + 1:]

def make_move(state, d):
    zeroloc = state.find('0')
    zeroi = zeroloc % grid_size
    zeroj = int((zeroloc % 4)/2)
    zerok = 1
    if(zeroloc <4):
        zerok = 0

    if d == 'up':
        return swap(state, zeroi, zeroj, zerok, zeroi, zeroj, zerok-1)
    elif d == 'down':
        return swap(state, zeroi, zeroj, zerok, zeroi, zeroj, zerok+1)
    elif d == 'left':
        return swap(state, zeroi, zeroj, zerok, zeroi-1, zeroj, zerok)
    elif d == 'right':
        return swap(state, zeroi, zeroj, zerok, zeroi+1, zeroj, zerok)
    elif d == 'forward':
        return swap(state, zeroi, zeroj, zerok, zeroi, zeroj+1, zerok)
    elif d == 'back':
        return swap(state, zeroi, zeroj, zerok, zeroi, zeroj-1, zerok)


def get_ij(state, i, j, k):
    return state[i + grid_size * j + grid_size**2*k]


class Node:
    def __init__(self, state=final_state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []


if __name__ == '__main__':
    main()