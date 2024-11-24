from parserFile import parser, data
from dataclasses import dataclass
from constants import *
import sys

"""
    Start state functionality from the project proposal
    Start state creates the initial problem state and fulfills all partial assignments (if any) from the input
    @return: Initial problem state 
"""
def start():
    # Parse the input
    parser(sys.argv)

    # Create the start state 
    pr = Problem(
        sched = Schedule(
            ## !!! RAY-Q why do we need a full schedule with invalid slots, we already have a list of the possible slots
            # !! RAY-Q don't see the point of coupling gameslots and practiceslots in the Slot class
            # Initialize the schedule with empty slots
            mo = [Slot() for i in range(27)],
            tu = [Slot() for i in range(27)],
            fr = [Slot() for i in range(27)]
        ),
        # Get the remaining games and practices
        remGames = data.Games.getGames(),
        remPracs = data.Practices.getPractices()
    )

    # !! RAY-Q this becomes unnecessary because only slots with gameMin/Maxes would be in sched
    # Where there are game slots, set game max and game min in pr to their corresponding values 
    for slot in data.GameSlots.getGameSlots():
        if (slot.getDay() == MO):
            pr.sched.mo[TIME[slot.getStartTime()]].game = ([], slot.getGameMax(), slot.getGameMin())
        elif (slot.getDay() == TU):
            pr.sched.tu[TIME[slot.getStartTime()]].game = ([], slot.getGameMax(), slot.getGameMin())
        elif (slot.getDay() == FR):
            pr.sched.fr[TIME[slot.getStartTime()]].game = ([], slot.getGameMax(), slot.getGameMin())

    # Where there are practice slots, set practice max and practice min in pr to their corresponding values 
    for slot in data.PracticeSlots.getPracticeSlots():
        if (slot.getDay() == MO):
            pr.sched.mo[TIME[slot.getStartTime()]].prac = ([], slot.getPracticeMax(), slot.getPracticeMin())
        elif (slot.getDay() == TU):
            pr.sched.tu[TIME[slot.getStartTime()]].prac = ([], slot.getPracticeMax(), slot.getPracticeMin())
        elif (slot.getDay() == FR):
            pr.sched.fr[TIME[slot.getStartTime()]].prac = ([], slot.getPracticeMax(), slot.getPracticeMin())
    
    # Fulfill partial assignments for games
    for game in data.Games.getGames():
        # Check if there is a partial assignment for the game
        slot = game.getPartialAssignmentSlot()
        if (slot != None): 
            day = None
            time = None
            # Get the day and time of the partial assignments slot
            if (slot.getDay() == MO):
                day = pr.sched.mo
                time = TIME[slot.getStartTime()] 
            elif (slot.getDay() == TU):
                day = pr.sched.tu
                time = TIME[slot.getStartTime()]
            else:
                day = pr.sched.fr
                time = TIME[slot.getStartTime()]

            # Check if the slot is valid using HC()
            if (HC(day[time].game, game)):
                # Add the game to the slot
                day[time].game[0].append(game)
                # Update the remaining games
                pr.remGames.remove(game)
            # If the slot is invalid, print an error and exit
            else: 
                print("Invalid slot for partial assignment; no valid assignment possible with HC")
                exit(1)

    # Fulfill partial assignments for practices   
    for prac in data.Practices.getPractices():        
        # Check if there is a partial assignment for the practice
        slot = prac.getPartialAssignmentSlot()
        if (slot != None): 
            day = None
            time = None
            # Get the day and time of the partial assignments slot
            if (slot.getDay() == MO):
                day = pr.sched.mo
                time = TIME[slot.getStartTime()] 
            elif (slot.getDay() == TU):
                day = pr.sched.tu
                time = TIME[slot.getStartTime()]
            else:
                day = pr.sched.fr
                time = TIME[slot.getStartTime()]

            # Check if the slot is valid using HC()
            if (HC(day[time].prac, prac)):
                # Add the practice to the slot
                day[time].prac[0].append(prac)
                # Update the remaining practices
                pr.remPracs.remove(prac)
            else:
                print("Invalid slot for partial assignment; no valid assignment possible with HC")
                exit(1)
    print(pr)
    return pr

"""
    Calculate hard constraints on a match for a given slot
    @param slot: Slot to check
    @param match: Game/practice to schedule
    @return: True if slot is valid, False otherwise
"""
def HC(slot, match):
    # Check if slot is valid based on hard constraints
    return True

start()
