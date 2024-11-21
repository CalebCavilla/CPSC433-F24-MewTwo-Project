from parser import parser, data
from dataclasses import dataclass
import sys

"""
    Dictionary to map time strings to integers
    If there is a simpler way to do this, please lmk
"""
time = {
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
    game: tuple[list[data.Game], int, int]
    practice: tuple[list[data.Practice], int, int]

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
    remGame: list[data.Game]
    remPrac: list[data.Practice]


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
            mo = [Slot(([], 0, 0), ([], 0, 0)) for i in range(27)],
            tu = [Slot(([], 0, 0), ([], 0, 0)) for i in range(27)],
            fr = [Slot(([], 0, 0), ([], 0, 0)) for i in range(27)]
        ),
        # Get the remaining games and practices
        remGame = data.Games.getGames(),
        remPrac = data.Practices.getPractices()
    )

    # Where there are game slots, set game max and game min in pr to their corresponding values 
    for gameSlot in data.GameSlots.getGameSlots():
        if (gameSlot.getDay() == 'MO'):
            pr.sched.mo[time[gameSlot.getStartTime()]].game = ([], gameSlot.getGameMax(), gameSlot.getGameMin())
        elif (gameSlot.getDay() == 'TU'):
            pr.sched.tu[time[gameSlot.getStartTime()]].game = ([], gameSlot.getGameMax(), gameSlot.getGameMin())
        elif (gameSlot.getDay() == 'FR'):
            pr.sched.fr[time[gameSlot.getStartTime()]].game = ([], gameSlot.getGameMax(), gameSlot.getGameMin())

    # Where there are practice slots, set practice max and practice min in pr to their corresponding values 
    for pracSlot in data.PracticeSlots.getPracticeSlots():
        if (pracSlot.getDay() == 'MO'):
            pr.sched.mo[time[pracSlot.getStartTime()]].practice = ([], pracSlot.getPracticeMax(), pracSlot.getPracticeMin())
        elif (pracSlot.getDay() == 'TU'):
            pr.sched.tu[time[pracSlot.getStartTime()]].practice = ([], pracSlot.getPracticeMax(), pracSlot.getPracticeMin())
        elif (pracSlot.getDay() == 'FR'):
            pr.sched.fr[time[pracSlot.getStartTime()]].practice = ([], pracSlot.getPracticeMax(), pracSlot.getPracticeMin())
    

    # Fullfill partial assignments here
    

    return pr

start()
