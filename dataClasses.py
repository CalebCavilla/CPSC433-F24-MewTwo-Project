import sys
import re

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

        words = str(self.identifier).split()
        self.organization = words[0]
        self.ageGroup = words[1]
        self.division = int(words[3])
    
    def __str__(self):
        return f"{self.identifier}"
    
    def __repr__(self):
        return f"{repr(self.identifier)}"
    
    def __eq__(self, other):
        if isinstance(other, Game):
            return self.identifier == other.identifier # Two games are considered the same if they have the same identifier
        return NotImplemented

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
    
    def addPreferenceSlot(self, gameSlot, preferenceValue):
        """
        add a slot to the games preference list
        
        Parameters
            gameSlot (GameSlot): the game slot that the game has a preference for
            preferenceValue (int): the preference value of the slot the game wants
        """
        self.preferenceSlots.append((gameSlot, preferenceValue))
    
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
    
    def getOrganization(self):
        """Returns the organization of the practice"""
        return self.organization
    
    def getAgeGroup(self):
        """Returns the age group of the practice"""
        return self.ageGroup
    
    def getDivision(self):
        """Returns the division of the practice"""
        return self.division
    
    

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

        words = self.identifier.split()
        self.organization = words[0]
        self.ageGroup = words[1]
         # Check for division and practice
        if "DIV" in words:
            self.division = int(words[words.index("DIV") + 1])
            if "PRC" in words:
                self.practiceNum = int(words[words.index("PRC") + 1])
            else:
                self.practiceNum = int(words[words.index("OPN") + 1])
        else:
            self.division = None
            if "PRC" in words:
                self.practiceNum = int(words[words.index("PRC") + 1])
            else:
                self.practiceNum = int(words[words.index("OPN") + 1])

    def __str__(self):
        return f"{self.identifier}"
    
    def __repr__(self):
        return f"{repr(self.identifier)}"
    
    def __eq__(self, other):
        if isinstance(other, Practice):
            return self.identifier == other.identifier # Two games are considered the same if they have the same identifier
        return NotImplemented

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
    
    def addPreferenceSlot(self, practiceSlot, preferenceValue):
        """
        add a slot to the practices preference list
        
        Parameters
            practiceSlot (PracticeSlot): the practice slot that the practice has a preference for
            preferenceValue (int): the preference value of the slot the practice wants
        """
        self.preferenceSlots.append((practiceSlot, preferenceValue))
    
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
    
    def getOrganization(self):
        """Returns the organization of the practice"""
        return self.organization
    
    def getAgeGroup(self):
        """Returns the age group of the practice"""
        return self.ageGroup
    
    def getDivision(self):
        """Returns the division of the practice"""
        return self.division
    
    def getPracticeNum(self):
        """Returns the practiceNum of the practice"""
        return self.practiceNum


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
    
    @staticmethod
    def getGameSlotByDayAndTime(day, startTime):
        """Returns a game slot in the list of current game slots if it is in the list, None otherwise
        
        Parameters:
            day (str): The day of the game slot you want to retrieve
            startTime (str): The start time of the game slot you want to retrieve
        """
        for gameSlot in GameSlots.gameSlots:
            if isinstance(gameSlot, GameSlot):
                if (gameSlot.getDay() == day and gameSlot.getStartTime() == startTime):
                    return gameSlot
        return None

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
    
    @staticmethod
    def getPracticeSlotByDayAndTime(day, startTime):
        """Returns a practice slot in the list of current practice slots if it is in the list, None otherwise
        
        Parameters:
            day (str): The day of the practice slot you want to retrieve
            startTime (str): The start time of the practice slot you want to retrieve
        """
        for practiceSlot in PracticeSlots.practiceSlots:
            if isinstance(practiceSlot, PracticeSlot):
                if (practiceSlot.getDay() == day and practiceSlot.getStartTime() == startTime):
                    return practiceSlot
        return None


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
    
    @staticmethod
    def getGameByIdentifier(identifier):
        """Returns a game in the list of current games if it is in the list, None otherwise
        
        Parameters:
            identifier (str): The identifier of the game you want to retrieve from the list of current games
        """
        for game in Games.games:
            if isinstance(game, Game):
                if game.getIdentifier() == identifier:
                    return game
        return None

    
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
    
    @staticmethod
    def getPracticeByIdentifier(identifier):
        """Returns a practice in the list of current practices if it is in the list, None otherwise
        
        Parameters:
            identifier (str): The identifier of the practice you want to retrieve from the list of current practices
        """
        for practice in Practices.practices:
            if isinstance(practice, Practice):
                if practice.getIdentifier() == identifier:
                    return practice
        return None
    
class WeightsAndPenalties:
    """
    Static Class to hold all weights and penalties needed for the search
    """
    minFilledWeight = None
    prefWeight = None
    pairWeight = None
    secDiffWeight = None
    gameMinPen = None
    practiceMinPen = None
    notPairedPen = None
    sectionPen = None

    @staticmethod
    def getMinFilledWeight():
        """Returns the minimum filled weight"""
        return WeightsAndPenalties.minFilledWeight
    
    @staticmethod
    def setMinFilledWeight(minFilledWeight):
        """sets the value of the minimum filled weight"""
        WeightsAndPenalties.minFilledWeight = minFilledWeight

    @staticmethod
    def getPrefWeight():
        """Returns the preference weight"""
        return WeightsAndPenalties.prefWeight
    
    @staticmethod
    def setPrefWeight(prefWeight):
        """sets the value of the preference weight"""
        WeightsAndPenalties.prefWeight = prefWeight

    @staticmethod
    def getPairWeight():
        """Returns the pair weight"""
        return WeightsAndPenalties.pairWeight
    
    @staticmethod
    def setPairWeight(pairWeight):
        """sets the value of the pair weight"""
        WeightsAndPenalties.pairWeight = pairWeight

    @staticmethod
    def getSecDiffWeight():
        """Returns the section difference weight"""
        return WeightsAndPenalties.secDiffWeight
    
    @staticmethod
    def setSecDiffWeight(secDiffWeight):
        """sets the value of the section difference weight"""
        WeightsAndPenalties.secDiffWeight = secDiffWeight
    
    @staticmethod
    def getGameMinPen():
        """Returns the game minimum penalty"""
        return WeightsAndPenalties.gameMinPen
    
    @staticmethod
    def setGameMinPen(gameMinPen):
        """sets the value of the game minimum penalty"""
        WeightsAndPenalties.gameMinPen = gameMinPen
    
    @staticmethod
    def getPracticeMinPen():
        """Returns the practice minimum penalty"""
        return WeightsAndPenalties.practiceMinPen
    
    @staticmethod
    def setPracticeMinPen(practiceMinPen):
        """sets the value of the practice minimum penalty"""
        WeightsAndPenalties.practiceMinPen = practiceMinPen

    @staticmethod
    def getNotPairedPen():
        """Returns the not paired penalty"""
        return WeightsAndPenalties.notPairedPen
    
    @staticmethod
    def setNotPairedPen(notPairedPen):
        """sets the value of the not paired penalty"""
        WeightsAndPenalties.notPairedPen = notPairedPen

    @staticmethod
    def getSectionPen():
        """Returns the section penalty"""
        return WeightsAndPenalties.sectionPen
    
    @staticmethod
    def setSectionPen(sectionPen):
        """sets the value of the section penalty"""
        WeightsAndPenalties.sectionPen = sectionPen



class InvalidInputError(Exception):
    def __init__(self, message):
        super().__init__(message)

