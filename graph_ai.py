import matplotlib.pyplot as plt

# Data
problem_states = ['Trivial', 'Very easy', 'Easy', 'Do able', 'Hard', 'Oh boy']
ucs_depth = [0, 1, 2, 4, 16, 22]
ucs_node_expanded = [0, 2, 3, 30, 10876, 85704]
a_tiles_depth = [0.0008, 0.0052, 0.0068, 0.0095, 16, 22]
a_tiles_node_expanded = [1, 3, 3, 4, 378, 3593]
a_manhattan_depth = [0.0002, 0.0046, 0.0052, 0.0079, 0.209, 0.6124]
a_manhattan_node_expanded = [1, 1, 2, 4, 158, 365]
ucs_time = [0, 0.0052, 0.0068, 0.0095, 101.39, 5533.01]
a_tiles_time = [0.0002, 0.0046, 0.0052, 0.0079, 1.03, 37.72]
a_manhattan_time = [0.0042, 0.0067, 0.0008, 0.0079, 0.209, 0.6124]
ucs_in_queue = [1, 5, 4, 20, 6180, 25040]
a_tiles_in_queue = [0, 3, 3, 4, 378, 3593]
a_manhattan_in_queue = [1, 3, 3, 4, 108, 223]


# Plotting the graph solution depth vs Node Expanded
plt.plot(ucs_depth, ucs_node_expanded, marker='o', label='UCS')
plt.plot(a_tiles_depth, a_tiles_node_expanded, marker='o', label='A* MisP')
plt.plot(a_manhattan_depth, a_manhattan_node_expanded, marker='o', label='A* Manhattan')

# Set labels and title
plt.xlabel('Solution Depth')
plt.ylabel('Node Expanded')
plt.title('Solution Depth vs. Node Expanded')

# Set legend
plt.legend()

# Show the graph
plt.show()




# Plotting the graph time taken by each algorithm for each problem 
plt.plot(problem_states, ucs_time, marker='o', label='UCS')
plt.plot(problem_states, a_tiles_time, marker='o', label='A* MisP')
plt.plot(problem_states, a_manhattan_time, marker='o', label='A* Manhattan')

# Set labels and title
plt.xlabel('Problem State')
plt.ylabel('Time (s)')
plt.title('Time taken by Algorithms')

# Set legend
plt.legend()

# Rotate x-axis labels for better visibility
plt.xticks(rotation=45)

# Show the graph
plt.show()




# Plotting the graph for Maximum Number Nodes in a Queue at a time
plt.plot(problem_states, ucs_in_queue, marker='o', label='UCS')
plt.plot(problem_states, a_tiles_in_queue, marker='o', label='A* MisP')
plt.plot(problem_states, a_manhattan_in_queue, marker='o', label='A* Manhattan')

# Set labels and title
plt.xlabel('Problem State')
plt.ylabel('Max Nodes in Queue')
plt.title('Maximum Number of Nodes in a Queue')

# Set legend
plt.legend()

# Rotate x-axis labels for better visibility
plt.xticks(rotation=45)

# Show the graph
plt.show()

