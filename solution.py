from parser import parser, data
from dataclasses import dataclass
import sys

MO = 'MO'
TU = 'TU'
FR = 'FR'
"""
    Dictionary to map time strings to integers
    If there is a simpler way to do this, please lmk
"""
TIME = {
    "8:00": 0, "8:30": 1, "9:00": 2, "9:30": 3,"10:00": 4,
    "10:30": 5, "11:00": 6, "11:30": 7, "12:00": 8, "12:30": 9,
    "13:00": 10, "13:30": 11, "14:00": 12, "14:30": 13, "15:00": 14,
    "15:30": 15, "16:00": 16, "16:30": 17, "17:00": 18, "17:30": 19,
    "18:30": 21, "19:00": 22, "19:30": 23, "20:00": 24, "20:30": 25, "21:00": 26
}

"""
    Slot class to represent a slot in the schedule
    game: tuple of (list of games, max games, min games)
    practice: tuple of (list of practices, max practices, min practices)
"""
@dataclass
class Slot:
    game: tuple[list[data.Game], int, int] = ([], 0, 0)
    prac: tuple[list[data.Practice], int, int] = ([], 0, 0)

"""
    Schedule class to represent the schedule
    mo: list of slots for monday
    tu: list of slots for tuesday
    fr: list of slots for friday
"""
@dataclass
class Schedule:
    mo: list[Slot] 
    tu: list[Slot] 
    fr: list[Slot] 


"""
    Problem class to represent a problem
    sched: A schedule
    remGame: list of remaining games
    remPrac: list of remaining practices
"""
@dataclass
class Problem:
    sched: Schedule 
    remGames: list[data.Game] 
    remPracs: list[data.Practice] 


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
            # Initialize the schedule with empty slots
            mo = [Slot() for i in range(27)],
            tu = [Slot() for i in range(27)],
            fr = [Slot() for i in range(27)]
        ),
        # Get the remaining games and practices
        remGames = data.Games.getGames(),
        remPracs = data.Practices.getPractices()
    )

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
                print("Invalid slot for partial assignment")
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
                print("Invalid slot for partial assignment")
                exit(1)
            
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
