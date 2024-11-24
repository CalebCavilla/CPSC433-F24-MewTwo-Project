"""
Authors: Enzo Mutiso (30182555)
CPSC433
References:
"""

"""
    Calculate the total penalty for minimum slot usage
    @author: Enzo Mutiso
    @param sched: Schedule to calculate the penalty for
    @param pen_gamemin: Penalty for minimum game slot usage
    @param pen_practicemin: Penalty for minimum practice slot usage
    @return: Total penalty for minimum slot usage
"""
def gpmin(sched, pen_gamemin, pen_practicemin):
    return 0

"""
    Calculate the total penalty for failed preference slots
    @author: Enzo Mutiso
    @param sched: Schedule to calculate the penalty for
    @return: Total penalty for failed preference slots
"""
def pref(sched):
    return 0

"""
    Calculate the total penalty for mismatched pairs of games/practices
    @author: Enzo Mutiso
    @param sched: Schedule to calculate the penalty for
    @param pen_notpaired: Penalty for each mismatched pair
    @return: Total penalty for mismatched pairs
"""
def pair(sched, pen_notpaired):
    return 0

"""
    Calculate the total penalty for pairs of games/practices from the same division
    @author Enzo Mutiso
    @param sched: Schedule to calculate the penalty for
    @param pen_section: Penalty for each division pair
    @return: Total penalty for division pairs
"""
def divisionPair(sched, pen_section):
    return 0