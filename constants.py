from dataclasses import dataclass, field
from typing import Dict
from parserFile import data

"""
    This file only contains necessary constants and data structures for problem representation
"""

"""
    Schedule class to represent the schedule
    gameslots: dict with 
                    key as a date-time string of gameSlots
                    value as list of games that have been scheduled then
    practSlots: dict with 
                    key as a date-time string of practiceSlots
                    value as list of practices that have been scheduled then
"""

@dataclass
class Schedule:
    gameSlots: Dict[str, list[str]] = field(default_factory=dict)
    pracSlots: Dict[str, list[str]] = field(default_factory=dict)


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