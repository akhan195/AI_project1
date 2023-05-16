import copy
import heapq
import time

class Node:
    def __init__(self, parent=None, state=0, cost_from_start=0, cost_to_goal=0, depth=0):
        self.parent = parent
        self.state = state
        self.cost_from_start = cost_from_start
        self.cost_to_goal = cost_to_goal
        self.depth = depth
        self.children = []
        
    def __eq__(self, other):
        return self.state == other.state
    
    def __lt__(self, other):
        return (self.cost_from_start + self.cost_to_goal) < (other.cost_from_start + other.cost_to_goal)

    def add_child(self, node, cost_to_expand=1):
        node.cost_from_start = self.cost_from_start + cost_to_expand
        node.parent = self
        node.depth = self.depth + 1
        self.children.append(node)
        
    def get_f_val(self):
        return self.cost_from_start + self.cost_to_goal
    
    def traceback(self):
        current = self
        path = []
        while current:
            path.append(current.state)
            current = current.parent
        path.reverse()
        print(f"{len(path)} nodes traced.")
        for state in path:
            print(state)
        print()
        
    def print_state(self):
        for row in self.state:
            print(row)
        
    def operator(self):
        def swap_and_append(i_zero, j_zero, i_swap, j_swap):
            tmp_state = copy.deepcopy(self.state)
            tmp_state[i_zero][j_zero], tmp_state[i_swap][j_swap] = tmp_state[i_swap][j_swap], tmp_state[i_zero][j_zero]
            return tmp_state
        
        i_zero, j_zero = find_in_sublists(0, self.state)
        state_len = len(self.state)
        
        states_to_return = []
        
        # Move Up
        if i_zero != 0:
            i_swap, j_swap = i_zero - 1, j_zero
            states_to_return.append(swap_and_append(i_zero, j_zero, i_swap, j_swap))
        
        # Move Right
        if j_zero != (state_len - 1):
            i_swap, j_swap = i_zero, j_zero + 1
            states_to_return.append(swap_and_append(i_zero, j_zero, i_swap, j_swap))
                
        # Move Down
        if i_zero != (state_len - 1):
            i_swap, j_swap = i_zero + 1, j_zero
            states_to_return.append(swap_and_append(i_zero, j_zero, i_swap, j_swap))
        
        # Move Left
        if j_zero != 0:
            i_swap, j_swap = i_zero, j_zero - 1
            states_to_return.append(swap_and_append(i_zero, j_zero, i_swap, j_swap))
        
        return states_to_return


def manhattan_distance_heuristic(state, goal):
    total_distance = 0

    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == goal[i][j]:
                continue

            if state[i][j] == 0:
                continue

            else:
                # Find the coordinates of this tile in the goal state
                goal_tile_i, goal_tile_j = find_in_sublists(state[i][j], goal)

                distance = abs(i - goal_tile_i) + abs(j - goal_tile_j)
                total_distance += distance

    return total_distance


def misplaced_tile_heuristic(state, goal):
    count = 0
    
    for i in range(len(goal)):
        for j in range(len(goal[i])):
            if state[i][j] != goal[i][j] and state[i][j] != 0:
                count += 1
            
    return count


def check_states_equal(state_a, state_b):
    """
    Check if two states are equal.

    Returns:
    True if states are the same, False otherwise.
    """
    rows_a = len(state_a)
    rows_b = len(state_b)

    if rows_a != rows_b:
        return False

    for i in range(rows_a):
        cols_a = len(state_a[i])
        cols_b = len(state_b[i])

        if cols_a != cols_b:
            return False

        for j in range(cols_a):
            if state_a[i][j] != state_b[i][j]:
                return False

    return True



def find_in_sublists(val, lst):
    """
    Helper function used to find a value in a list of lists.
    
    Returns:
    A tuple containing the indices (i, j) of val in lst.
    If the value is not found, (None, None) is returned.
    """
    for i, sub_list in enumerate(lst):
        try:
            j = sub_list.index(val)
            return i, j
        except ValueError:
            continue
    
    return None, None

def general_search(problem, heuristic):
    """
    General search algorithm based on the pseudo code provided. Based on the input search_algorithm - {UCS, A* Misp, A* Manhattan} is passed as the value for the parameter of "heuristic".
    """
    initial_node = Node(state=problem['init_state'])
    priority_queue = []
    heapq.heappush(priority_queue, initial_node)
    explored_nodes = []

    output_enabled = True
    max_queue_size = 1
    expanded_count = 0

    while priority_queue:
        max_queue_size = max(len(priority_queue), max_queue_size)

        current_node = heapq.heappop(priority_queue)

        if output_enabled:
            print("\nThe best state to expand with g(n) = " + str(int(current_node.cost_from_start)) +
                  " and h(n) = " + str(int(current_node.cost_to_goal)) + " is...")
            current_node.print_state()

        if check_states_equal(current_node.state, problem['goal_state']):
            if output_enabled:
                print("\nFound a solution!")
                print("Traceback:")
                current_node.traceback()
                print("To solve this problem, the search algorithm expanded a total of " + str(expanded_count) + " nodes.")
                print("The maximum number of nodes in the queue: " + str(max_queue_size))
                print("Depth of the optimal solution: " + str(current_node.depth))  # Print the depth of the solution

            return expanded_count, max_queue_size

        else:
            explored_nodes.append(current_node)

            expanded_states_list = [state for state in current_node.operator() if state is not None]

            if not expanded_states_list:
                continue

            for expanded_state in expanded_states_list:
                new_node = Node(state=expanded_state)

                if (priority_queue and new_node in priority_queue) or (explored_nodes and new_node in explored_nodes):
                    # Node already visited
                    continue

                if heuristic == "a_star_misplaced":
                    new_node.cost_to_goal = misplaced_tile_heuristic(new_node.state, problem['goal_state'])

                if heuristic == "a_star_manhattan":
                    new_node.cost_to_goal = manhattan_distance_heuristic(new_node.state, problem['goal_state'])

                current_node.add_child(node=new_node)

                heapq.heappush(priority_queue, new_node)

            expanded_count += 1

    print("Failure: Unable to find a solution")
    return -1


def get_algorithm():
    """
     Getting the  search algorithm - as a input from the user 
    """
    print("Select algorithm:\n"
          + " 1 Uniform Cost Search" + "\n"
          + " 2 A* Misplaced Tile Heuristic" + "\n"
          + " 3 A* Manhattan Distance Heuristic" + "\n"
    )

    options = {
        "1": ("uniform", "Uniform Cost Search"),
        "2": ("a_star_misplaced", "A* Misplaced Tile Heuristic"),
        "3": ("a_star_manhattan", "A* Manhattan Distance Heuristic"),
    }

    while True:
        try:
            user_input = input() or str(len(options))

            if int(user_input) < 1 or int(user_input) > len(options):
                print("Error: Input " + user_input + " is not within the valid range.\n")
                raise ValueError

            break
        except ValueError:
            print("Error: Please input a number within the valid range or press enter for the default option!")

    print("Selected algorithm: " + options[user_input][1])

    return options[user_input][0]


def init_default_puzzle():
    """
    Hardcoded the various usecases of problem statement for evaluating the performance of the algorithms
    """
 
    
    puzzle_list = [
        ("trivial", [[1, 2, 3], [4, 5, 6], [7, 8, 0]]),
        ("very easy", [[1, 2, 3], [4, 5, 6], [7, 0, 8]]),
        ("easy", [[1, 2, 0], [4, 5, 3], [7, 8, 6]]),
        ("doable", [[0, 1, 2], [4, 5, 3], [7, 8, 6]]),
        ("oh boy", [[8, 7, 1], [6, 0, 2], [5, 4, 3]]),
        ("hard", [[1, 6, 7], [5, 0, 3], [4, 8, 2]]),
    ]
    
    list_len = len(puzzle_list)

    print("Default puzzle: enter the difficulty (1 to " + str(list_len) + "):\n")
    
    
    for i, puzzle in enumerate(puzzle_list):
        print(f" [{i + 1}] {puzzle[0]}")
    
    while True:
        try:
            selected_difficulty = int(input() or 1)

            if selected_difficulty < 1 or selected_difficulty > list_len:
                print("Error: input " + str(selected_difficulty) + " is not within range.\n")
                raise ValueError

            break
        except ValueError:
            print("Error: Please input valid choice")

    
    print("Selected " + puzzle_list[selected_difficulty - 1][0] + "\n")
    return puzzle_list[selected_difficulty - 1][1]

def get_goal_state(num_rows):
    """
    Customizing the Goal state as desired by user
    """
    default_goal_state = [[(j + 1) + (num_rows * i) for j in range(num_rows)] for i in range(num_rows)]
    default_goal_state[num_rows - 1][num_rows - 1] = 0

    print("Use default goal state? [y]/n")

    for row in default_goal_state:
        print(row)

    goal_mode = input() or "y"

    if goal_mode.lower() != "y":
        print("Please enter the desired goal state."
              + " Delimit the numbers with a space. Press enter when done.\n")

        custom_goal_state = []

        # Get custom goal state
        for i in range(num_rows):
            row_input = input("Enter row number " + str(i + 1) + ": ").split()
            row = [int(x) for x in row_input]  # Convert input values to integers
            custom_goal_state.append(row)

        
        zero_exists, _ = find_in_sublists(0, custom_goal_state)
        if not zero_exists:
            print("No 0 found. Exiting...")
            return None

        return custom_goal_state

    return default_goal_state

def get_initial_state(num_rows):
    """
    Directly taking the input for the intial state of puzzle instead of hardcode one as we have done in default  function - init_default_puzzle()
    """
    print("Enter puzzle's initial state."
          + " Delimit the numbers with a space. Press enter when done.\n")

    initial_state = []

    # Get custom start state
    for i in range(num_rows):
        row_input = input("Enter row number " + str(i + 1) + ": ").split()
        row_values = [int(x) for x in row_input]  # Convert input values to integers
        initial_state.append(row_values)

    # Check for existence of 0
    zero_exists, _ = find_in_sublists(0, initial_state)
    if not zero_exists:
        print("No 0 found. Exiting...")
        return None

    return initial_state




def main():
    print("Select an option:\n")
    print("[1] Default 3x3 puzzle" + "\n"
          + "[2] Custom puzzle" + "\n"
          + "(Press enter to default to [1])"
    )

    initial_state = []
    goal_state = []
    problem = {}

    while True:
        user_choice = input() or "1"

        if user_choice == "1":
            initial_state = init_default_puzzle()
            goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
            problem['init_state'] = initial_state
            problem['goal_state'] = goal_state
            break

        if user_choice == "2":
            print("Customize Puzzle: Enter the row x column dimension")

            while True:
                try:
                    num_rows = int(input())

                    if num_rows <= 0:
                        raise ValueError

                    break
                except ValueError:
                    print("Error: Please input a positive number")

            initial_state = get_initial_state(num_rows)
            if initial_state is None:
                return

            goal_state = get_goal_state(num_rows)
            if goal_state is None:
                return

            problem['init_state'] = initial_state
            problem['goal_state'] = goal_state

            break
        else:
            print("Please input 1, 2, or press enter for default.")

    selected_algorithm = get_algorithm()
    t1_start = time.perf_counter()
    # Start the search algorithm
    general_search(problem, selected_algorithm)

    t1_stop = time.perf_counter()
    execution_time_ms = (t1_stop - t1_start) 
    print("--- %s milliseconds ---" % execution_time_ms)

    return

main()