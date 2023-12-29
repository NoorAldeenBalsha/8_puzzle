from copy import deepcopy

DIRECTIONS = {"UP": [-1, 0], "DOWN": [1, 0], "LEFT": [0, -1], "RIGHT": [0, 1]}

class Node:
    def __init__(self, current_node, previous_node, g, h, dir):
        self.current_node = current_node
        self.previous_node = previous_node
        self.g = g
        self.h = h
        self.dir = dir

    def f(self):
        return self.g + self.h

def get_pos(current_state, element):
    for row in range(len(current_state)):
        if element in current_state[row]:
            return (row, current_state[row].index(element))

def misplaced_tiles_cost(current_state, end_state):
    cost = 0
    for row in range(len(current_state)):
        for col in range(len(current_state[0])):
            if current_state[row][col] != end_state[row][col]:
                cost += 1
    return cost

def manhattan_distance_cost(current_state, end_state):
    cost = 0
    for row in range(len(current_state)):
        for col in range(len(current_state[0])):
            element = current_state[row][col]
            if element != 0:
                goal_pos = get_pos(end_state, element)
                cost += abs(row - goal_pos[0]) + abs(col - goal_pos[1])
    return cost

def get_adjacent_nodes(node, end_state, heuristic):
    list_nodes = []
    empty_pos = get_pos(node.current_node, 0)

    for dir in DIRECTIONS.keys():
        new_pos = (empty_pos[0] + DIRECTIONS[dir][0], empty_pos[1] + DIRECTIONS[dir][1])
        if 0 <= new_pos[0] < len(node.current_node) and 0 <= new_pos[1] < len(node.current_node[0]):
            new_state = deepcopy(node.current_node)
            new_state[empty_pos[0]][empty_pos[1]] = node.current_node[new_pos[0]][new_pos[1]]
            new_state[new_pos[0]][new_pos[1]] = 0

            list_nodes.append(Node(new_state, node.current_node, node.g + 1, heuristic(new_state, end_state), dir))

    return list_nodes
   
def get_best_node(open_set):
    first_iter = True
    best_f = None
    best_node = None

    for node in open_set.values():
        if first_iter or node.f() < best_f:
            first_iter = False
            best_node = node
            best_f = best_node.f()
    return best_node

def build_path(closed_set, end_state):
    node = closed_set[str(end_state)]
    path = []

    while node.dir:
        path.append({
            'dir': node.dir,
            'node': node.current_node
        })
        node = closed_set[str(node.previous_node)]
    path.append({
        'dir': '',
        'node': node.current_node
    })
    path.reverse()

    return path

def main_program():
    start_state = [[1, 2, 3], [0, 4, 5], [6, 7, 8]]
    end_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    print("Initial State:")
    for row in start_state:
        print(row)
        
    print("Goal state is:")
    for row in end_state:
        print(row)
    print()    

    misplaced_tiles, misplaced_tiles_solution = main_algorithm(start_state, end_state, misplaced_tiles_cost)
    num_misplaced_tiles_moves = len(misplaced_tiles_solution) - 1
    print("Expanded nodes to solve using Misplaced Tiles heuristic:", misplaced_tiles)
    print(f"Total Moves using Misplaced Tiles heuristic: {num_misplaced_tiles_moves}")
    manhattan_distance, manhattan_distance_solution = main_algorithm(start_state, end_state, manhattan_distance_cost)
    num_manhattan_distance_moves = len(manhattan_distance_solution) - 1
    print("Expanded nodes to solve using Manhattan Distance heuristic:", manhattan_distance)
    print(f"Total Moves using Manhattan Distance heuristic: {num_manhattan_distance_moves}")

def main_algorithm(start_state, end_state, heuristic):
    open_set = {str(start_state): Node(start_state, start_state, 0, heuristic(start_state, end_state), "")}
    closed_set = {}

    expanded_nodes = 0

    while True:
        test_node = get_best_node(open_set)
        closed_set[str(test_node.current_node)] = test_node
        expanded_nodes += 1

        if test_node.current_node == end_state:
            return expanded_nodes, build_path(closed_set, end_state)

        adjacent_nodes = get_adjacent_nodes(test_node, end_state, heuristic)
        for node in adjacent_nodes:
            if str(node.current_node) in closed_set.keys() or (str(node.current_node) in open_set.keys() and open_set[str(node.current_node)].f() < node.f()):
                continue
            open_set[str(node.current_node)] = node

        del open_set[str(test_node.current_node)]

main_program()