# General code structure for AND tree

"""
    Main code loop for AND tree search algorithm
    @param prob: Initial problem state 
    @return: Solution to the problem
"""
def treeSearch(prob):
    # Initially, prob is a list of the initial problem state
    # Insert prob into max heap and calculate SC()? 
    heap = []

    # Loop until we cannot generate any more leaves
    while True:
        # Run Fleaf to choose the best leaf node
        pr = fleaf(heap)
        # Run Ftrans to choose a game or practice to schedule
        match = ftrans()
        # Run DIV to create leafs based on ftrans and pr
        div(pr, match)

    return 0

"""
    Generates a list of new leaf nodes based on the given leaf node.
    DIV will only generate VALID leaf nodes. 
    Valid leaf nodes are leaf nodes that satisfy the hard constraints
    @param pr: Leaf node to generate new leaf nodes from 
    @param match: Game or practice to schedule
    @return: List of new valid schedules (leafs)
"""
def div(pr, match):
    # Look through all open slots in leaf and check if that slot is valid or not based on hard constraints
    # If it is valid, generate a new leaf node with match in that slot, append it to the list of new leaf nodes
    # Return the list of new leaf nodes

    # IDEA
        # If max heap is used in fleaf, DIV may need to use SC() to calculate soft constraint values for new leafs and add them to the heap here
        # fleaf will simply pop the max value from the heap to get the best leaf node; does not call SC() 
    return 0

"""
    Chooses the best leaf node from the max heap
    @param heap: Max heap of leaf nodes
    @return: Chosen best leaf node
"""
def fleaf(heap):
    # IDEA
        # Use max heap to store the leaf node soft constraint values, pop the max value to get the best leaf node
        # Must calculate soft constraint values for new leafs generated in DIV
    return 0  
    
""" 
    Chooses a game or practice to schedule from the list of remaining games/practices 
    Will choose a game or practice in the order of:
        Highest preference value (Random in case of tied preference values)
        Random game or practice that want to be scheduled as a pair
        Random game or practice 
    @param rem: list of remaining games/practices to be scheduled 
    @return game or practice to schedule
"""
def ftrans(rem):
    
    return 0


