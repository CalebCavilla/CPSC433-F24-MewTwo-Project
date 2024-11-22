from dataclasses import dataclass
from parserFile import data

"""
    This file only contains necessary constants and data structures for problem representation
"""

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