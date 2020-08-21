import random
import time
import heapq
from collections import deque

final_state = 'ABCDEFGHIJKLMNO0'
grid_size = 4
do = ['up', 'down', 'left', 'right']
possible_moves = {0: ['down', 'right'], 1: ['down', 'left', 'right'], 2: ['down', 'left', 'right'], 3: ['down', 'left'], \
4: ['up', 'down', 'right'], 5: ['up', 'down', 'left', 'right'], 6: ['up', 'down', 'left', 'right'], 7: ['up', 'down', 'left'], \
8: ['up', 'down', 'right'], 9: ['up', 'down', 'left', 'right'], 10: ['up', 'down', 'left', 'right'], 11: ['up', 'down', 'left'], \
12: ['up', 'right'], 13: ['up', 'left', 'right'], 14: ['up', 'left', 'right'], 15: ['up', 'left']}

visited_states = set()


def main():
    string = input()
    print(string)
    solve = iddfs(Node(string, 1, None))
    print(string + " " + str(solve.depth) )


def output_test():
    print('A possible solvable puzzle: ' + make_puzzle(Node()))
    string = input('Input a 9char solvable puzzle: ')
    tic = time.time()
    solved_node = bfssolve(Node(string, 1, None))
    toc = time.time()
    print(str(toc - tic) + ' seconds')
    result = 'LENGTH: ' + str(path(solved_node))
    print('PUZZLE: ' + string + '\t' + result)


def file_output():
    file = open('puzzle.txt', 'r')
    tic = time.time()
    for line in file.read().splitlines():
        a = bfssolve(Node(line, 1, None))
        print('PUZZLE: ' + line + '\t' + 'LENGTH: ' + str(a.depth))
        visited_states.clear()
    toc = time.time()
    print(toc - tic)


def manhattan_test():
    ll = list(final_state)
    random.shuffle(ll)
    tic = time.time()
    for x in range(10000):
        heuristic(Node(''.join(ll)))
        random.shuffle(ll)
    toc = time.time()
    print(toc - tic)


def heuristic(node):
    distance = 0
    count1 = 0
    count2 = 0
    dictionary = {}
    for c in final_state:
        dictionary[c] = count1
        count1 += 1
    for x in node.state:
        distance += abs(dictionary[x] // grid_size - count2 // grid_size) + abs(
            dictionary[x] % grid_size - count2 % grid_size)
        count2 += 1
    return distance


def greedy(state):
    visited_states.clear()
    visited_states.add(state.state)
    fringe = []
    heapq.heappush(fringe, (0, state))
    while fringe:
        v = heapq.heappop(fringe)
        if v[1].state == final_state:
            return v[1]
        for d in possible_moves[v[1].state.find('0')]:
            temp = make_move(v[1].state, d)
            if temp not in visited_states:
                child = Node(temp, v[1].depth + 1, v[1])
                if not (child is None):
                    v[1].children.append(child)
                    visited_states.add(child.state)
                    heapq.heappush(fringe, (heuristic(child) + child.depth, child))
    return None


def dfs(state, depth=22):
    fringe = [(state, set())]
    count = 1
    while fringe:
        v = fringe.pop()
        if v[0].state == final_state:
            print(count)
            return v[0]
        for d in possible_moves[v[0].state.find('0')]:
            temp = make_move(v[0].state, d)
            if temp not in visited_states and v[0].depth < depth:
                child = Node(temp, v[0].depth + 1, v)
                count += 1
                if child is not None and child.state not in v[1]:
                    v[0].children.append(child)
                    v[1].add(v[0].state)
                    fringe.append((child, v[1]))
    return None



def bfs(state):
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
                child = Node(temp, v.depth + 1, v)
                if not (child is None):
                    v.children.append(child)
                    visited_states.add(child.state)
                    fringe.append(child)
    return None

def iddfs(state):
    for k in range(1, 81):
        visited_states = {state.state}
        fringe = [state]
        start_node = dfs(state, k)
        if start_node is not None and start_node.state == final_state:
            return start_node
    return None

def bidirbfs(state):
    visited_start = {state.state}
    visited_goal = {final_state}
    startfringe = deque()
    goalfringe = deque()
    startfringe.append(state)
    goalfringe.append(Node())
    while startfringe:
        startfringe= fringe.pop()


def path(state):
    if state is None:
        for x in range(grid_size):
            print(state.state[x * grid_size:x * grid_size + grid_size])
        return 0
    elif state.parent is None:
        for x in range(grid_size):
            print(state.state[x * grid_size:x * grid_size + grid_size])
        return 1
    else:
        count = 1 + path(state.parent)
        print('\n')
        for x in range(grid_size):
            print(state.state[x * grid_size:x * grid_size + grid_size])
        return count


def make_puzzle(grid):
    a = random.randint(20, 100)
    for x in range(a):
        temp = make_move(grid.state, random.choice(do))
        if temp is not None:
            grid.state = temp
    return grid.state


def swap(state, zi, zj, di, dj):
    if min(di, dj) < 0 or grid_size <= max(di, dj):
        return None
    value = get_ij(state, di, dj)
    zeroindex = zi * grid_size + zj
    dindex = di * grid_size + dj
    if zeroindex < dindex:
        return state[:zeroindex] + value + state[zeroindex + 1: dindex] + '0' + state[dindex + 1:]
    else:
        return state[:dindex] + '0' + state[dindex + 1: zeroindex] + value + state[zeroindex + 1:]


def make_move(state, d):
    zeroloc = state.find('0')
    zeroj = zeroloc % grid_size
    zeroi = int(zeroloc / grid_size)
    if d == 'up':
        return swap(state, zeroi, zeroj, zeroi - 1, zeroj)
    elif d == 'down':
        return swap(state, zeroi, zeroj, zeroi + 1, zeroj)
    elif d == 'left':
        return swap(state, zeroi, zeroj, zeroi, zeroj - 1)
    elif d == 'right':
        return swap(state, zeroi, zeroj, zeroi, zeroj + 1)


def get_ij(state, i, j):
    return state[i * grid_size + j]


class Node:
    def __init__(self, state=final_state, depth=1, parent=None):
        self.state = state
        self.parent = parent
        self.depth = depth
        self.children = []

    def __lt__(self, other):
        return 0


if __name__ == '__main__':
    main()
