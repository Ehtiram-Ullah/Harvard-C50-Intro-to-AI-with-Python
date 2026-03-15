"Author: Ehtiram Ullah"


"""
State
-----
Represents the state stored inside a node.

A state can represent anything (location, configuration, etc.).
For simplicity, this implementation stores only a single character.
"""
class State:
    def __init__(self, char):
        self.char = char

    def getState(self):
        return self.char



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
Goal Test
---------
Determines whether the given state satisfies the goal condition.

In this example, the goal state is 'E'.
"""
def goalTest(state: State):
    return state.char == "E"



"""
Path Reconstruction
-------------------
Reconstructs the path from the current node back to the root node.

Process:
1. Start from the goal node.
2. Follow the parent pointers upward.
3. Construct the path in reverse order (goal → root).
4. Reverse the string so it appears as root → goal.
"""
def trackPath(node: Node):
    path = ""

    while node != None:
        path += node.state.char

        # Add a connection indicator if there is a parent
        if node.parent != None:
            path += " >--- "

        node = node.parent

    # Reverse because the path was constructed backwards
    return path[::-1]



"""
Search Algorithm
----------------
Performs a depth-first traversal of the graph to find the path
with the lowest total cost that reaches the goal state.

During traversal:
• The path cost is accumulated.
• When a goal state is reached, the cost is compared
  with the current optimal cost.
• If the new path is cheaper, it becomes the new optimal path.
"""
def search(node: Node, pathCost=0):
    global optimalPath
    global optimalCost

    # Stop if node does not exist
    if node == None:
        return
    
    # Accumulate path cost while traversing
    pathCost += node.pathCost

    # Check if the current node satisfies the goal
    if goalTest(node.state):

   

        if pathCost < optimalCost:
            optimalPath = trackPath(node)
            optimalCost = pathCost

            # Reset local cost after updating optimal solution
            pathCost = 0

 


    # Continue searching through both actions
    search(node.leftNode, pathCost)
    search(node.rightNode, pathCost)



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


# Root node reference
tmp = n1


# Variables used to store the optimal solution
optimalCost = float('inf')
optimalPath = ""


# Start search from root
search(n1)


# Output result
print(f'Optimal Cost: {optimalCost}')
print(f'Optimal Path: {optimalPath}')