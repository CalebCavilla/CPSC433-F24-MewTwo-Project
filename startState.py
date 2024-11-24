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
            # Initialize the schedule with parsed game and practice slots
            gameSlots= {key: [] for key in data.GameSlots.gameSlotsDict.keys()},
            pracSlots= {key: [] for key in data.PracticeSlots.practiceSlotsDict.keys()}
        ),
        # Get the remaining games and practices
        remGames = data.Games.getGames(),
        remPracs = data.Practices.getPractices()
    )

    # Fulfill partial assignments for games
    for game in pr.remGames:
        preferredSlot = game.getPartialAssignmentSlot()

        ## !!! RAY-A this is as simple as adding a game to a slot would be
        if (preferredSlot):
            if (HC(pr.sched, preferredSlot.id, game.identifier)):
                pr.sched.gameSlots[preferredSlot.id].append(game.identifier)
                pr.remGames.remove(game)
            else:
                raise print(f"Invalid slot for partial assignment; no valid assignment possible with HC")

    for prac in pr.remPracs:
        preferredSlot = prac.getPartialAssignmentSlot()

        ## !!! RAY-A this is as simple as adding a prac to a slot would be
        if (preferredSlot):
            if (HC(pr.sched, preferredSlot.id, prac.identifier)):
                pr.sched.pracSlots[preferredSlot.id].append(prac.identifier)
                pr.remPracs.remove(prac)
            else:
                raise print(f"Invalid slot for partial assignment; no valid assignment possible with HC")

    print(pr)
    return pr

"""
    Calculate hard constraints on a match for a given slot
    @param sched: Complete schedule to check against
    @param slotToCheck: The slot to which a game/practice is being added
    @param match: Specific game/practice that is being added
    @return: True if slot is valid, False otherwise
"""
def HC(sched, slotToCheck, match):
    # Check if slot is valid based on hard constraints
    return True

start()
