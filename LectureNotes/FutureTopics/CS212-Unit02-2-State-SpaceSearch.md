<h1>State-Space Search Algorithm</h1>

A state-space search algorithm solves a problem by systematically exploring a **state space**, which is a mathematical representation of all possible configurations (states) and transitions (actions) within the problem.

## Core Concepts

The algorithm fundamentally works with three main components:

### 1. States and State Space

- **State:** A snapshot of the problem at any given time. For the missionaries and cannibals problem, a state is defined by the number of missionaries and cannibals on each river bank and the boat's location. For airline scheduling, a state might include the current assignment of all aircraft to routes, their locations, and departure times.
- **Initial State:** The configuration where the problem begins (e.g., all missionaries and cannibals on the starting bank).
- **Goal State:** The desired final configuration (e.g., all missionaries and cannibals on the opposite bank, or a complete, optimized flight schedule).
- **State Space:** The entire collection of all possible states and the connections between them, often visualized as a **graph** .

### 2. Actions and Transitions

- **Action (or Operator):** A permissible move that changes the current state. In the river crossing problem, an action is moving a specific combination of people across the river. In scheduling, an action could be assigning a specific aircraft to an available route at a given time.
- **Transition:** The move from one state to a new state resulting from an action. This forms the edges in the state-space graph.

### 3. The Search Process

The algorithm begins at the **initial state** and searches the state space graph to find a sequence of valid actions (a path) that leads to the **goal state**.

1. **Exploration:** The algorithm maintains a set of **unexplored states** (often called the **"frontier"** or **"open list"**). It repeatedly selects a state from this set.
2. **Expansion:** The algorithm applies all possible, valid **actions** to the selected state, generating its successor (or "child") states.
3. **Testing:** Each newly generated state is checked to see if it is the **goal state**.
4. **Tracking:** If a state isn't the goal, it is added to the frontier to be explored later. The algorithm also keeps track of the **path** taken to reach each state to eventually reconstruct the solution.
5. **Termination:** The search continues until the goal state is found (the solution is the path from the initial state to the goal state), or until the frontier is empty (meaning no solution exists).

This is a specialized application of the Breadth-First search:

**Breadth-First Search (BFS)**: This algorithm is one way of solving this problem without trying all the combinations of legal transitions. It explores all possible states level by level. It starts from the initial state and explores all possible moves, then moves to the next level of states. BFS guarantees finding the shortest path (minimum number of river crossings) to the goal state because it explores all nodes at the present depth level before moving on to nodes at the next depth level.

## Generalization and Efficiency

The efficiency and behavior of the algorithm depend heavily on its **search strategy** (e.g., Breadth-First Search, Depth-First Search, A* Search):

- **Uninformed Search:** These strategies only use information about the problem structure (like which states are connected) and are generally slower (e.g., trying all possibilities).
- **Informed (Heuristic) Search:** These strategies, such as **A\***, use a **heuristic function** (![img](data:,)) to estimate the *cost* or *distance* from the current state (![img](data:,)) to the goal state. This allows the algorithm to prioritize exploring states that seem "closer" to the goal, dramatically speeding up the search for complex, real-world problems like airline scheduling. The algorithm often calculates the total estimated cost of a path as ![img](data:,), where ![img](data:,) is the cost of the path *from* the start state *to* the current state ![img](data:,).

In essence, the state-space search algorithm transforms a complex problem into a problem of **finding the shortest or cheapest path in a graph**. 

## Solution to the Zombies and Humans River Crossing Problem

This Python program implements the **Breadth-First Search (BFS)** algorithm to find the shortest path solution to the "Zombies and Humans" problem, exactly as described in your document. BFS is guaranteed to find the shortest path in terms of the number of moves (transitions).

```python
import collections

# --- Problem Definitions based on the provided document ---

# State representation: (H, Z, B)
# H = Humans on the starting bank (0 to 3)
# Z = Zombies on the starting bank (0 to 3)
# B = Boat location (1 for starting bank, 0 for other bank)

INITIAL_STATE = (3, 3, 1)
GOAL_STATE = (0, 0, 0)
MAX_PEOPLE = 3  # Three humans and three zombies in total

# --- Core Logic Functions ---

def is_valid_state(h, z):
    """
    Checks the safety constraint for both banks.
    Constraint: Zombies must not outnumber humans on either bank, unless humans = 0.

    Bank 1 (Starting Bank): h humans, z zombies
    Bank 2 (Other Bank): (MAX_PEOPLE - h) humans, (MAX_PEOPLE - z) zombies
    """
    # Check Bank 1
    # Condition: If there are humans (h > 0), zombies (z) must not be greater than humans (z <= h).
    if h > 0 and z > h:
        return False

    # Check Bank 2 (Other Bank)
    h_other = MAX_PEOPLE - h
    z_other = MAX_PEOPLE - z
    # Condition: If there are humans on the other bank (h_other > 0), 
    # zombies on the other bank (z_other) must not be greater than humans (z_other <= h_other).
    if h_other > 0 and z_other > h_other:
        return False

    # Check bounds (must have between 0 and MAX_PEOPLE on the starting bank)
    if not (0 <= h <= MAX_PEOPLE and 0 <= z <= MAX_PEOPLE):
        return False

    # Boat must always have a position (1 or 0)
    # The boat check is handled in the 'get_possible_moves' function later.

    return True

def get_possible_moves():
    """
    Defines the 5 possible transition types (people moving in the boat).
    These are represented as (delta_H, delta_Z).
    The boat capacity is 1 or 2 people, with at least 1 person.
    """
    # (Humans, Zombies) in the boat
    moves = [
        (1, 0),  # 1 human
        (2, 0),  # 2 humans
        (0, 1),  # 1 zombie
        (0, 2),  # 2 zombies
        (1, 1)   # 1 human, 1 zombie
    ]
    return moves

def get_next_states(current_state):
    """
    Generates all valid successor states from the current state.
    """
    H, Z, B = current_state
    next_states = []

    # Get the movement factor:
    # If B=1 (boat on starting bank), the boat moves to the other side (B -> 0), 
    # and people (h_move, z_move) LEAVE the starting bank (subtracted). Factor = 1.
    # If B=0 (boat on other bank), the boat moves to the starting bank (B -> 1), 
    # and people (h_move, z_move) RETURN to the starting bank (added). Factor = -1.
    
    # We use 'factor' to determine whether the move adds or subtracts from (H, Z)
    # Factor = 1: people move from Bank 1 to Bank 2 (H -= h_move, Z -= z_move)
    # Factor = -1: people move from Bank 2 to Bank 1 (H += h_move, Z += z_move)
    factor = 1 if B == 1 else -1

    for h_move, z_move in get_possible_moves():
        # A move is valid ONLY IF the people being moved are available on the current boat bank
        
        # Calculate people on the boat's current bank (the bank they are leaving from)
        if B == 1:
            # Leaving from Bank 1 (Starting Bank)
            h_available = H
            z_available = Z
        else:
            # Leaving from Bank 2 (Other Bank)
            h_available = MAX_PEOPLE - H
            z_available = MAX_PEOPLE - Z

        # Check if the required people are available to make the move
        if h_move <= h_available and z_move <= z_available:
            
            # Calculate the new state (H', Z', B')
            H_new = H - (h_move * factor)
            Z_new = Z - (z_move * factor)
            B_new = 1 - B # Flip boat position

            # Check if the new state is valid and within bounds
            if is_valid_state(H_new, Z_new):
                next_states.append((H_new, Z_new, B_new))

    return next_states

def solve_zombie_crossing():
    """
    Uses Breadth-First Search (BFS) to find the shortest path solution.
    """
    # Queue for BFS: stores (state, path_to_state)
    queue = collections.deque([(INITIAL_STATE, [INITIAL_STATE])])
    
    # Set to keep track of visited states to avoid cycles and redundant work
    visited = {INITIAL_STATE}
    
    # Run the BFS
    while queue:
        current_state, path = queue.popleft()

        # Check for goal state
        if current_state == GOAL_STATE:
            return path # Found the shortest path!

        # Explore successor states
        for next_state in get_next_states(current_state):
            if next_state not in visited:
                visited.add(next_state)
                # Create a new path by appending the next_state
                new_path = path + [next_state]
                queue.append((next_state, new_path))
    
    return None # No solution found

# --- Execution and Output ---

solution_path = solve_zombie_crossing()

if solution_path:
    print("--- Zombie and Human River Crossing Solution ---")
    print(f"Initial State: {INITIAL_STATE}")
    print(f"Goal State:    {GOAL_STATE}")
    print(f"Solution Found in {len(solution_path) - 1} moves:\n")

    # Format and print the solution path
    for i, state in enumerate(solution_path):
        h, z, b = state
        step_number = i
        
        # Calculate people on the other bank for display purposes
        h_other = MAX_PEOPLE - h
        z_other = MAX_PEOPLE - z
        
        boat_location = "START Bank" if b == 1 else "OTHER Bank"

        # Determine the action taken to get to this state (not possible for step 0)
        action_desc = "START"
        if i > 0:
            prev_state = solution_path[i-1]
            prev_h, prev_z, prev_b = prev_state
            
            # Calculate change in H and Z (relative to starting bank)
            h_diff = prev_h - h
            z_diff = prev_z - z

            # Determine direction
            direction = "Start -> Other" if prev_b == 1 else "Other -> Start"

            # Reconstruct the move
            if prev_b == 1:
                # Move was from start to other, so h_diff and z_diff are positive (or zero)
                action_desc = f"Move {abs(h_diff)} H, {abs(z_diff)} Z {direction}"
            else:
                # Move was from other to start, so h_diff and z_diff are negative (or zero)
                action_desc = f"Move {abs(h_diff)} H, {abs(z_diff)} Z {direction}"


        print(f"STEP {step_number:02d} | Action: {action_desc}")
        print(f"      Start Bank: {h} Humans, {z} Zombies")
        print(f"      Other Bank: {h_other} Humans, {z_other} Zombies (Boat: {boat_location})")
        print("-" * 40)
        
    print(f"Solution completed in {len(solution_path) - 1} moves.")
else:
    print("No solution found for the Zombie Crossing problem.")

```

