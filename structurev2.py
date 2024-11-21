# General code structure for AND tree
# V2 does not use a max heap to store the best leaf nodes in order
# Soft constraints will only be calculated after the algorithm finds all solutions 
# Fleaf will choose a leaf with breadth/depth or random selection
# End result will be the same as V1 but with less computation on calculating leaf values

incompatible = [] # List of incompatible games/practices
unwanted = [] # List of unwanted games/practices
preferences = [] # List of preferences for games/practices
pairs = [] # List of games/practices that want to be scheduled together

"""
    Node class to store the schedule and remaining games/practices
    Is equivalent to one pr from the ATree proposal
"""
class Node:
    # Note: Could change depending on how the parser is implemented
    def __init__(self, schedule, remaining):
        self.schedule = schedule
        self.remaining = remaining

"""
    Main code loop for AND tree search algorithm
    @param prob: Initial problem state
    @return: Solution to the problem
"""
def treeSearch(prob):
    # Initially, prob is a list of the initial problem state
    leafs = [] # Contains all leaf nodes in the tree
    solutions = [] # Contains all potential solutions to the problem

    # Loop until we cannot generate any more leaves
    while True:
        # Run Fleaf
        pr = fleaf(leafs)

        # remove pr from leafs
        leafs.remove(pr)

        # Run Ftrans to choose a game or practice to schedule
        match = ftrans(pr)

        # Remove match from remaining 
        pr[1].remove(match)

        # Run DIV to create leafs based on ftrans and pr
        newLeafs = div(pr, match)

        # If no new leafs are generated, pr is a solution
        # Additionally, we will only consider pr as a "real" solution if there are no remaining games/practices
        if len(newLeafs) == 0 & len(pr.remaining) == 0:
            solutions.append(pr)
        # Add new leafs to leafs
        leafs += newLeafs

        # If leafs is empty, break out of loop
        if len(leafs) == 0:
            break

    # Choose the best leaf from leafs using SC()
    best = SC(solutions)
    
    # Return the best leaf
    return best

"""
    Generates a list of new leaf nodes based on the given leaf node
    DIV will only generate VALID leaf nodes
    Valid leaf nodes are leaf nodes that satisfy the hard constraints
    @param pr: Leaf node to generate new leaf nodes from
    @param match: Game or practice to schedule
    @return: List of new valid schedules (leafs)
"""
def div(pr, match):
    newLeafs = [] # Contains all new leafs that DIV generates

    # Look through all open slots in the leaf and check if it is valid or not based on hard constraints HC()
    # If it is valid, generate a new leaf node with match in that slot
    # Append the new leaf to newLeafs

    # Return the list of new leaf nodes
    return newLeafs

""" 
    Choose a leaf node from the list of leaf nodes
    @param leafs: list of leaf nodes
    @return: Chosen leaf node
"""
def fleaf(leafs):
    # In V2, we are not choosing a leaf based on soft constraints
    # Decision can be made via breadth/depth/random or whatever we come up with

    # Return a leaf node
    return leaf

"""
    Choose a game or practice to schedule from the list of remaining games/practices
    Will choose a game or practice in the order of:
        Highest preference value (Random between tied preference values)
        Random game or practice that want to be scheduled as a pair
        Random game or practice
    @param pr: pr from fleaf. 
    @return game or practice to schedule
"""
def ftrans(pr):
    remaining = pr.remaining 

    # Choose a game or practice from preferences
    # If none, choose a game or practice from pairs
    # If none, choose a random game or practice
    return match

"""
    Calculate hard constraints for a given slot
    @param slot: Slot to check
    @param match: Game/practice to schedule
    @return: True if slot is valid, False otherwise
"""
def HC(slot, match):
    # Check if slot is valid based on hard constraints
    return True

"""
    Calculate soft constraints for all solutions
    @param solutions: List of solutions
    @return: Best solution 
"""
def SC(solutions):
    # Calculate soft constraints for all solutions
    
    # Loop through all solutions and calculate the soft constraints 
        # gpmin 
            # for each slot, the number of games/practices scheduled should be greater than or equal to the minimum 
        # pref
            # look at each game/practice from preferences and see if it is scheduled in that time
        # atgame 
            # Different divisional games within a single age/tier group should be scheduled at different times


    # Return the best solution
    return 0
