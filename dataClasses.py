import sys

class GameSlot:
    """
    Class to represent a game slot in the schedule

    Attributes:
        day (str): Identifier for the day of the week the slot is in ("MO", "TU", "FR")
        startTime (str): Time of the day that the game slot is in (Ex. "8:00", "14:30")
        gameMax (int): maximum number of games that can be scheduled into this slot
        gameMin (int): minimum number of games that can be scheduled into this slot
    """
    def __init__(self, day, startTime, gameMax, gameMin):
        self.day = day
        self.startTime = startTime
        self.gameMax = gameMax
        self.gameMin = gameMin

    def __str__(self):
        return f"[{self.day}, {self.startTime}, {self.gameMax}, {self.gameMin}]"
    
    def __repr__(self):
        return f"[{repr(self.day)}, {repr(self.startTime)}, {repr(self.gameMax)}, {repr(self.gameMin)}]"

    def getDay(self):
        """Returns the day of the week as a string"""
        return self.day
    
    def getStartTime(self):
        """Returns the start time during the day as a string"""
        return self.startTime
    
    def getGameMax(self):
        """Returns the maximum number of games for the time slot as an int"""
        return self.gameMax
    
    def getGameMin(self):
        """Returns the minimum number of games for the time slot as an int"""
        return self.gameMin


class PracticeSlot:
    """
    Class to represent a practice slot in the schedule

    Attributes:
        day (str): Identifier for the day of the week the slot is in ("MO", "TU", "FR")
        startTime (str): Time of the day that the practice slot is in (Ex. "8:00", "14:30")
        practiceMax (int): maximum number of practice that can be scheduled into this slot
        practiceMin (int): minimum number of practice that can be scheduled into this slot
    """
    def __init__(self, day, startTime, practiceMax, practiceMin):
        self.day = day
        self.startTime = startTime
        self.practiceMax = practiceMax
        self.practiceMin = practiceMin

    def __str__(self):
        return f"[{self.day}, {self.startTime}, {self.practiceMax}, {self.practiceMin}]"
    
    def __repr__(self):
        return f"[{repr(self.day)}, {repr(self.startTime)}, {repr(self.practiceMax)}, {repr(self.practiceMin)}]"

    def getDay(self):
        """Returns the day of the week as a string"""
        return self.day
    
    def getStartTime(self):
        """Returns the start time during the day as a string"""
        return self.startTime
    
    def getPracticeMax(self):
        """Returns the maximum number of practices for the time slot as an int"""
        return self.practiceMax
    
    def getPracticeMin(self):
        """Returns the minimum number of practices for the time slot as an int"""
        return self.practiceMin
    

class Game:
    """
    Class to represent a game that needs to be scheduled

    Attributes:
        identifier (str): the label for the game (Ex. "CMSA U13T3 DIV 01")
    """
    def __init__(self, identifier):
        self.identifier = identifier
        self.incompatibilities = []
        self.unwantedSlots = []
        self.preferenceSlots = []
        self.pairs = []
        self.partialAssignSlot = None
    
    def __str__(self):
        return f"{self.identifier}"
    
    def __repr__(self):
        return f"{repr(self.identifier)}"

    def getIdentifier(self):
        """Returns the identifier for the game as a string"""
        return self.identifier
        
    def addIncompatibility(self, element):
        """
        add an element to the games incompatibility list
        
        Parameters
            element (Game/Practice): the game/practice that is not compatible with the game
        """
        self.incompatibilities.append(element)
    
    def getIncompatibility(self):
        """Returns a copy of the list of games/practices the game is not compatible with"""
        return list(self.incompatibilities)
    
    def addUnwantedSlot(self, gameSlot):
        """
        add a slot to the games unwanted list
        
        Parameters
            gameSlot (GameSlot): the game slot that the game does not want
        """
        self.unwantedSlots.append(gameSlot)
    
    def getUnwantedSlots(self):
        """Returns a copy of the list of game slots that the game does not want"""
        return list(self.unwantedSlots)
    
    def addPreferenceSlot(self, gameSlot):
        """
        add a slot to the games preference list
        
        Parameters
            gameSlot (GameSlot): the game slot that the game has a preference for
        """
        self.preferenceSlots.append(gameSlot)
    
    def getPreferenceSlots(self):
        """Returns a copy of the list of game slots that the game has a preference for"""
        return list(self.preferenceSlots)
    
    def addPair(self, element):
        """
        add an element to the list of elements the game is paired with
        
        Parameters
            element (Game/Practice): the game/practice that is to be paired with the game
        """
        self.pairs.append(element)
    
    def getPairs(self):
        """Returns a copy of the list of games/practices the game is paired with"""
        return list(self.pairs)
    
    def setPartialAssignmentSlot(self, gameSlot):
        """
        add a slot that the game must be assigned to
        
        Parameters
            gameSlot (GameSlot): the game slot that the game must be assigned to
        """
        self.partialAssignSlot = gameSlot
    
    def getPartialAssignmentSlot(self):
        """Returns a copy of the game slot that the game is assigned to"""
        return self.partialAssignSlot
    
    

class Practice:
    """
    Class to represent a practice that needs to be scheduled

    Attributes:
        identifier (str): the label for the practice (Ex. "CMSA U13T3 DIV 01 PRC 01")
    """
    def __init__(self, identifier):
        self.identifier = identifier
        self.incompatibilities = []
        self.unwantedSlots = []
        self.preferenceSlots = []
        self.pairs = []
        self.partialAssignSlot = None

    def __str__(self):
        return f"{self.identifier}"
    
    def __repr__(self):
        return f"{repr(self.identifier)}"

    def getIdentifier(self):
        """Returns the identifier for the practice as a string"""
        return self.identifier
    
    def addIncompatibility(self, element):
        """
        add an element to the practices incompatibility list
        
        Parameters
            element (Game/Practice): the game/practice that is not compatible with the practice
        """
        self.incompatibilities.append(element)
    
    def getIncompatibility(self):
        """Returns a copy of the list of games/practices the practice is not compatible with"""
        return list(self.incompatibilities)
    
    def addUnwantedSlot(self, practiceSlot):
        """
        add a slot to the practice unwanted list
        
        Parameters
            practiceSlot (PracticeSlot): the practice slot that the practice does not want
        """
        self.unwantedSlots.append(practiceSlot)
    
    def getUnwantedSlots(self):
        """Returns a copy of the list of practice slots that the practice does not want"""
        return list(self.unwantedSlots)
    
    def addPreferenceSlot(self, practiceSlot):
        """
        add a slot to the practices preference list
        
        Parameters
            practiceSlot (PracticeSlot): the practice slot that the practice has a preference for
        """
        self.preferenceSlots.append(practiceSlot)
    
    def getPreferenceSlots(self):
        """Returns a copy of the list of practice slots that the practice has a preference for"""
        return list(self.preferenceSlots)
    
    def addPair(self, element):
        """
        add an element to the list of games/practices the practice is paired with
        
        Parameters
            element (Game/Practice): the game/practice that is to be paired with the practice
        """
        self.pairs.append(element)
    
    def getPairs(self):
        """Returns a copy of the list of games/practices the practice is paired with"""
        return list(self.pairs)
    
    def setPartialAssignmentSlot(self, practiceSlot):
        """
        add a slot that the practice must be assigned to
        
        Parameters
            practiceSlot (PracticeSlot): the practice slot that the practice must be assigned to
        """
        self.partialAssignSlot = practiceSlot
    
    def getPartialAssignmentSlot(self):
        """Returns a copy of the practice slot that the practice is assigned to"""
        return self.partialAssignSlot


class GameSlots:
    """
    Static Class to represent the list of all game slots available in the schedule
    """
    gameSlots = []

    @staticmethod
    def addGameSlot(gameSlot):
        """Adds a game slot to the current list of game slots
        
        Parameters:
            gameSlot (GameSlot): The game slot object to be added to the list of game slots
        """
        GameSlots.gameSlots.append(gameSlot)

    @staticmethod
    def removeGameSlot(gameSlot):
        """Remove a game slot from the current list of game slots
        
        Parameters:
            gameSlot (GameSlot): The game slot object to be removed from the list of game slots
        """
        GameSlots.gameSlots = [gs for gs in GameSlots.gameSlots if gs != gameSlot]

    @staticmethod
    def getGameSlots():
        """Returns a copy of the list of game slots available in the schedule"""
        return list(GameSlots.gameSlots)

class PracticeSlots:
    """
    Static Class to represent the list of all practice slots available in the schedule
    """
    practiceSlots = []

    @staticmethod
    def addPracticeSlot(practiceSlot):
        """Adds a practice slot to the current list of practice slots
        
        Parameters:
            practiceSlot (PracticeSlot): The practice slot object to be added to the list of practice slots
        """
        PracticeSlots.practiceSlots.append(practiceSlot)

    @staticmethod
    def removePracticeSlot(practiceSlot):
        """Remove a practice slot from the current list of practice slots
        
        Parameters:
            practiceSlot (Practice Slot): The practice slot object to be removed from the list of practice slots
        """
        PracticeSlots.practiceSlots = [ps for ps in PracticeSlots.practiceSlots if ps != practiceSlot]

    @staticmethod
    def getPracticeSlots():
        """Returns a copy of the list of practice slots available in the schedule"""
        return list(PracticeSlots.practiceSlots)


class Games:
    """
    Static Class to represent the list of all games that need to be scheduled
    """
    games = []

    @staticmethod
    def addGame(game):
        """Adds a game to the current list of games
        
        Parameters:
            game (Game): The game object to be added to the list of games
        """
        Games.games.append(game)

    @staticmethod
    def removeGame(game):
        """Remove a game from the current list of games
        
        Parameters:
            game (Game): The game object to be removed from the list of games
        """
        Games.games = [g for g in Games.games if g != game]

    @staticmethod
    def getGames():
        """Returns a copy of the list of games that needs to be scheduled"""
        return list(Games.games)
    
class Practices:
    """
    Static Class to represent the list of all practices that need to be scheduled
    """
    practices = []

    @staticmethod
    def addPractice(practice):
        """Adds a practice to the current list of practices
        
        Parameters:
            practice (Practice): The practice object to be added to the list of practices
        """
        Practices.practices.append(practice)

    @staticmethod
    def removePractice(practice):
        """Remove a practice from the current list of practices
        
        Parameters:
            practice (Practice): The practice object to be removed from the list of practices
        """
        Practices.practices = [p for p in Practices.practices if p != practice]

    @staticmethod
    def getPractices():
        """Returns a copy of the list of practices that needs to be scheduled"""
        return list(Practices.practices)

class InvalidInputError(Exception):
    def __init__(self, message):
        super().__init__(message)

