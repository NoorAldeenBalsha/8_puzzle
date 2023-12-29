import random
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


# Function to generate a random instance of the game
def generate_random_instance():
    numbers = list(range(9))
    random.shuffle(numbers)
    return [numbers[:3], numbers[3:6], numbers[6:]]

# Function to calculate the effective branching factor for a given depth and heuristic
def calculate_ebf(depth, heuristic):
    total_branching_factor = 0
    num_instances = 100

    for _ in range(num_instances):
        start_state = generate_random_instance()
        end_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

        open_set = {str(start_state): Node(start_state, start_state, 0, heuristic(start_state, end_state), "")}
        closed_set = {}

        expanded_nodes = 0

        while True:
            test_node = get_best_node(open_set)
            closed_set[str(test_node.current_node)] = test_node
            expanded_nodes += 1

            if test_node.current_node == end_state or test_node.g == depth:
                total_branching_factor += len(open_set)
                break

            adjacent_nodes = get_adjacent_nodes(test_node, end_state, heuristic)
            for node in adjacent_nodes:
                if str(node.current_node) in closed_set.keys() or (str(node.current_node) in open_set.keys() and open_set[str(node.current_node)].f() < node.f()):
                    continue
                open_set[str(node.current_node)] = node

            del open_set[str(test_node.current_node)]

    effective_branching_factor = total_branching_factor / num_instances
    return effective_branching_factor

# Calculate the effective branching factor for each depth and heuristic
depths = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
print("Depth\tEBF Misplaced tiles\tEPF Manhattan distance")
for depth in depths:
    ebf1=calculate_ebf(depth ,manhattan_distance_cost)
    ebf2=calculate_ebf(depth ,misplaced_tiles_cost)
    print(f"{depth}\t{ebf1}\t\t\t{ebf2}")