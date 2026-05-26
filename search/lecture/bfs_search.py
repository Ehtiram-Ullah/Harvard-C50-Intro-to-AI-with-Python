"""
Author: Ehtiram Ullah

Breadth First Search (BFS)
--------------------------
This program demonstrates BFS on a small graph.

The algorithm:
1. Starts from a root node.
2. Explores nodes level by level.
3. Checks for goal states.
4. Tracks the minimum-cost path to the goal.

Note:
BFS normally guarantees the shortest path in terms of
number of edges, NOT minimum cost.

This implementation still calculates path costs and
stores the cheapest goal found during traversal.
"""

from collections import deque


"""
State
-----
Represents the value stored inside a node.

A state can represent:
- a location
- a configuration
- a game state
- etc.

For simplicity, this example uses a single character.
"""
class State:
    def __init__(self, value):
        self.value = value

    # This will return the value when we put this inside print e.g print(State('A'))
    def __str__(self):
        return self.value
   



"""
Node
----
Represents a node in the search graph.

Each node stores:
• state      → The state associated with this node
• parent     → The node from which this node was reached
• leftNode   → Child node reached by the "left" action
• rightNode  → Child node reached by the "right" action
• pathCost   → Cost of moving from the parent node to this node

The methods 'left' and 'right' represent **actions** applied to a node.
Executing one of these actions creates a connection to another node.
"""
class Node:
    def __init__(self, state: State):
        self.state = state
        self.parent = None

        # Children nodes reachable through actions
        self.rightNode = None
        self.leftNode = None

        # Cost from parent to this node
        self.pathCost = 0


    """
    Action: RIGHT
    -------------
    Connects the current node to another node through a right action.

    node → destination node
    cost → cost of taking this action
    """
    def right(self, node, cost):
        self.rightNode = node
        node.parent = self
        node.pathCost = cost


    """
    Action: LEFT
    ------------
    Connects the current node to another node through a left action.

    node → destination node
    cost → cost of taking this action
    """
    def left(self, node, cost):
        self.leftNode = node
        node.parent = self
        node.pathCost = cost

"""
goal_test()
-----------
Checks whether the current state satisfies the goal condition.
"""
def goal_test(state: State):
    return state.value == "E"


"""
reconstruct_path()
------------------
Builds the path from root to goal node.

Example:
A -> C -> E
"""
def reconstruct_path(node: Node):
    path = []

    while node is not None:
        path.append(node.state.value)
        node = node.parent

    path.reverse()

    return " -> ".join(path)


"""
find_total_cost()
-----------------
Calculates total path cost from root to current node.
"""
def find_total_cost(node: Node):
    total_cost = 0

    while node is not None:
        total_cost += node.pathCost
        node = node.parent

    return total_cost


"""
bfs_search()
------------
Performs Breadth First Search.

Returns:
- best_path
- best_cost
"""
def bfs_search(start_node: Node):

    # Queue for BFS
    queue = deque([start_node])

    # Prevent revisiting nodes
    visited = set()

    best_path = None
    best_cost = float("inf")

    while queue:

        current_node = queue.popleft()
        

        # Skip already visited states
        if current_node.state.value in visited:
            continue

        visited.add(current_node.state.value)

        print(f"Visiting Node: {current_node.state.value}")

        # Goal check
        if goal_test(current_node.state):

            current_cost = find_total_cost(current_node)

            if current_cost < best_cost:
                best_cost = current_cost
                best_path = reconstruct_path(current_node)

        # Add children to queue
        if(current_node.leftNode):
            queue.append(current_node.leftNode)
        if(current_node.rightNode):
            queue.append(current_node.rightNode)
    

    return best_path, best_cost


# ------------------------------------------------
# Graph Construction
# ------------------------------------------------

n1 = Node(State("A"))
n2 = Node(State("B"))
n3 = Node(State("C"))
n4 = Node(State("D"))
n5 = Node(State("E"))


# Define actions between nodes
n1.left(n2, 3)
n1.right(n3, 2)

n3.left(Node(State('E')), 1)

n2.left(n4, 4)

n4.left(Node(State('E')), 1)



# ------------------------------------------------
# Run BFS
# ------------------------------------------------

optimal_path, optimal_cost = bfs_search(n1)


# ------------------------------------------------
# Output
# ------------------------------------------------

print("\nFinal Result")
print("------------")

if optimal_path:
    print(f"Optimal Cost : {optimal_cost}")
    print(f"Optimal Path : {optimal_path}")
else:
    print("Goal node not found.")