import sys
import dataClasses as data
from datetime import datetime

def is_time_in_range(timeStr):
    """Helper function to check if a time is in-between 8:00 - 21:00
    
    Parameters:
        timeStr (str): The time to check
    """
    try:
        # get a datetime object out of the string
        time = datetime.strptime(timeStr, "%H:%M").time()
        
        # Valid range of times
        startTime = datetime.strptime("08:00", "%H:%M").time()
        endTime = datetime.strptime("21:00", "%H:%M").time()
        
        # Check if the time is within range
        return startTime <= time <= endTime and time.minute in {0, 30}  # Make sure minutes are 0 or 30
    except ValueError:
        return False

def parser(searchInput):
    """Runs the parser on given input from the parser
    
    Parameters:
        searchInput (list): Should be the command line input sys.argv
    """
    try:
        if len(searchInput) != 10: raise data.InvalidInputError(f"Command line contains incorrect number of parameters, should be 9")
    except data.InvalidInputError as e:
        print(f"Caught Invalid Input Error: {e}")
        sys.exit()

    commandLineInputs = searchInput[1:] # get the list of inputs from the command line not including the main file name
    headers = ["Name:", "Game slots:", "Practice slots:", "Games:", "Practices:", "Not compatible:", "Unwanted:", "Preferences:", "Pair:", "Partial assignments:"]
    currentHeader = None

    try:
        with open(commandLineInputs[0], 'r') as file:
            for lineNum, line in enumerate(file, start=1):
                strippedLine = line.strip()

                if not strippedLine: # Skip empty lines
                    continue

                if strippedLine in headers:
                    currentHeader = strippedLine[:-1]
                elif currentHeader == "Name":
                    pass
                elif currentHeader == "Game slots":
                    words = [word.strip() for word in strippedLine.split(",")] # get the individual words out of the line

                    # Invalid Input checking
                    if (len(words) != 4): raise data.InvalidInputError(f"Header: (Game Slots) has an input with incorrect number of parameters, line: {lineNum}")
                    if (words[0] not in ["MO", "TU", "FR"]): raise data.InvalidInputError(f"Header: (Game Slots) has an input with invalid day label, line: {lineNum}")
                    if not is_time_in_range(words[1]): raise data.InvalidInputError(f"Header: (Game Slots) has an input with invalid time label, line: {lineNum}")
                    if not words[2].isdigit(): raise data.InvalidInputError(f"Header: (Game Slots) has an input with invalid gameMax, line: {lineNum}")
                    if not words[3].isdigit(): raise data.InvalidInputError(f"Header: (Game Slots) has an input with invalid gameMin, line: {lineNum}")

                    day = words[0]
                    time = words[1]
                    gameMax = int(words[2])
                    gameMin = int(words[3])
                    gameSlot = data.GameSlot(day, time, gameMax, gameMin)
                    data.GameSlots.addGameSlot(gameSlot)
                elif currentHeader == "Practice slots":
                    words = [word.strip() for word in strippedLine.split(",")] # get the individual words out of the line

                    # Invalid Input checking
                    if (len(words) != 4): raise data.InvalidInputError(f"Header: (Practice Slots) has an input with incorrect number of parameters, line: {lineNum}")
                    if (words[0] not in ["MO", "TU", "FR"]): raise data.InvalidInputError(f"Header: (Practice Slots) has an input with invalid day label, line: {lineNum}")
                    if not is_time_in_range(words[1]): raise data.InvalidInputError(f"Header: (Practice Slots) has an input with invalid time label, line: {lineNum}")
                    if not words[2].isdigit(): raise data.InvalidInputError(f"Header: (Practice Slots) has an input with invalid gameMax, line: {lineNum}")
                    if not words[3].isdigit(): raise data.InvalidInputError(f"Header: (Practice Slots) has an input with invalid gameMin, line: {lineNum}")

                    day = words[0]
                    time = words[1]
                    practiceMax = int(words[2])
                    practiceMin = int(words[3])
                    practiceSlot = data.PracticeSlot(day, time, practiceMax, practiceMin)
                    data.PracticeSlots.addPracticeSlot(practiceSlot)
                elif currentHeader == "Games":
                    words = strippedLine.split()
                    if (len(words) != 4): raise data.InvalidInputError(f"Header: (Games) has an input with incorrect number of parameters, line: {lineNum}")
                    game = data.Game(strippedLine)
                    data.Games.addGame(game)
                elif currentHeader == "Practices":
                    words = strippedLine.split()
                    if (len(words) != 4 and len(words) != 6): raise data.InvalidInputError(f"Header: (Practices) has an input with incorrect number of parameters, line: {lineNum}")
                    practice = data.Practice(strippedLine)
                    data.Practices.addPractice(practice)
                elif currentHeader == "Not compatible":
                    words = [word.strip() for word in strippedLine.split(",")] # get the individual words out of the line
                    if (len(words) != 2): raise data.InvalidInputError(f"Header: (Not compatible) has an input with incorrect number of parameters, line: {lineNum}")
                    element1 = words [0]
                    element2 = words [1]
                    if (data.Games.getGameByIdentifier(element1) != None and data.Games.getGameByIdentifier(element2) != None): # Both elements are games
                        game1 = data.Games.getGameByIdentifier(element1)
                        game2 = data.Games.getGameByIdentifier(element2)
                        game1.addIncompatibility(game2)
                        game2.addIncompatibility(game1)
                    elif (data.Games.getGameByIdentifier(element1) != None and data.Practices.getPracticeByIdentifier(element2) != None): # First element is game, second is practice
                        game1 = data.Games.getGameByIdentifier(element1)
                        practice1 = data.Practices.getPracticeByIdentifier(element2)
                        game1.addIncompatibility(practice1)
                        practice1.addIncompatibility(game1)
                    elif (data.Practices.getPracticeByIdentifier(element1) != None and data.Games.getGameByIdentifier(element2) != None): # first element is practice, second is game
                        practice1 = data.Practices.getPracticeByIdentifier(element1)
                        game1 = data.Games.getGameByIdentifier(element2)
                        practice1.addIncompatibility(game1)
                        game1.addIncompatibility(practice1)
                    elif (data.Practices.getPracticeByIdentifier(element1) != None and data.Practices.getPracticeByIdentifier(element2) != None): # Both elements are practices
                        practice1 = data.Practices.getPracticeByIdentifier(element1)
                        practice2 = data.Practices.getPracticeByIdentifier(element2)
                        practice1.addIncompatibility(practice2)
                        practice2.addIncompatibility(practice1)
                    else:
                        raise data.InvalidInputError(f"Header: (Preferences) has an input with a game/practice that does not exist, line: {lineNum}")
                elif currentHeader == "Unwanted":
                    words = [word.strip() for word in strippedLine.split(",")] # get the individual words out of the line
                    if (len(words) != 3): raise data.InvalidInputError(f"Header: (Unwanted) has an input with incorrect number of parameters, line: {lineNum}")
                    element = words[0]
                    slotDay = words[1]
                    slotTime = words[2]
                    if (data.Games.getGameByIdentifier(element) != None): # If its a game
                        game = data.Games.getGameByIdentifier(element)
                        slot = data.GameSlots.getGameSlotByDayAndTime(slotDay, slotTime)
                        if (slot == None): raise data.InvalidInputError(f"Header: (Unwanted) has an input with a slot that does not exist, line: {lineNum}")
                        game.addUnwantedSlot(slot)
                    elif(data.Practices.getPracticeByIdentifier(element) != None): # If its a practice
                        practice = data.Practices.getPracticeByIdentifier(element)
                        slot = data.PracticeSlots.getPracticeSlotByDayAndTime(slotDay, slotTime)
                        if (slot == None): raise data.InvalidInputError(f"Header: (Unwanted) has an input with a slot that does not exist, line: {lineNum}")
                        practice.addUnwantedSlot(slot)
                    else:
                        raise data.InvalidInputError(f"Header: (Unwanted) has an input with a game/practice that does not exist, line: {lineNum}")
                elif currentHeader == "Preferences":
                    words = [word.strip() for word in strippedLine.split(",")] # get the individual words out of the line
                    if (len(words) != 4): raise data.InvalidInputError(f"Header: (Preferences) has an input with incorrect number of parameters, line: {lineNum}")
                    slotDay = words[0]
                    slotTime = words[1]
                    element = words[2]
                    preferenceValue = words[3]
                    if (data.Games.getGameByIdentifier(element) != None): # If its a game
                        game = data.Games.getGameByIdentifier(element)
                        slot = data.GameSlots.getGameSlotByDayAndTime(slotDay, slotTime)
                        if (slot == None): print(f"WARNING, Header: (Preferences) has an input with a slot that does not exist, line: {lineNum}"); continue
                        game.addPreferenceSlot(slot, preferenceValue)
                    elif(data.Practices.getPracticeByIdentifier(element) != None): # If its a practice
                        practice = data.Practices.getPracticeByIdentifier(element)
                        slot = data.PracticeSlots.getPracticeSlotByDayAndTime(slotDay, slotTime)
                        # you can have invalid slots for some reason in preference input, just ignore and pass
                        if (slot == None): print(f"WARNING, Header: (Preferences) has an input with a slot that does not exist, line: {lineNum}"); continue
                        practice.addPreferenceSlot(slot, preferenceValue)
                    else:
                        print(data.InvalidInputError(f"WARNING Header: (Preferences) has an input with a game/practice that does not exist, line: {lineNum}"))
                elif currentHeader == "Pair":
                    words = [word.strip() for word in strippedLine.split(",")] # get the individual words out of the line
                    if (len(words) != 2): raise data.InvalidInputError(f"Header: (Pair) has an input with incorrect number of parameters, line: {lineNum}")
                    element1 = words [0]
                    element2 = words [1]
                    if (data.Games.getGameByIdentifier(element1) != None and data.Games.getGameByIdentifier(element2) != None): # Both elements are games
                        game1 = data.Games.getGameByIdentifier(element1)
                        game2 = data.Games.getGameByIdentifier(element2)
                        game1.addPair(game2)
                        game2.addPair(game1)
                    elif (data.Games.getGameByIdentifier(element1) != None and data.Practices.getPracticeByIdentifier(element2) != None): # First element is game, second is practice
                        game1 = data.Games.getGameByIdentifier(element1)
                        practice1 = data.Practices.getPracticeByIdentifier(element2)
                        game1.addPair(practice1)
                        practice1.addPair(game1)
                    elif (data.Practices.getPracticeByIdentifier(element1) != None and data.Games.getGameByIdentifier(element2) != None): # first element is practice, second is game
                        practice1 = data.Practices.getPracticeByIdentifier(element1)
                        game1 = data.Games.getGameByIdentifier(element2)
                        practice1.addPair(game1)
                        game1.addPair(practice1)
                    elif (data.Practices.getPracticeByIdentifier(element1) != None and data.Practices.getPracticeByIdentifier(element2) != None): # Both elements are practices
                        practice1 = data.Practices.getPracticeByIdentifier(element1)
                        practice2 = data.Practices.getPracticeByIdentifier(element2)
                        practice1.addPair(practice2)
                        practice2.addPair(practice1)
                    else:
                        raise data.InvalidInputError(f"Header: (Pair) has an input with a game/practice that does not exist, line: {lineNum}")
                elif currentHeader == "Partial assignments":
                    words = [word.strip() for word in strippedLine.split(",")] # get the individual words out of the line
                    if (len(words) != 3): raise data.InvalidInputError(f"Header: (Partial assignments) has an input with incorrect number of parameters, line: {lineNum}")
                    element = words[0]
                    slotDay = words[1]
                    slotTime = words[2]
                    if (data.Games.getGameByIdentifier(element) != None): # If its a game
                        game = data.Games.getGameByIdentifier(element)
                        slot = data.GameSlots.getGameSlotByDayAndTime(slotDay, slotTime)
                        if (slot == None): raise data.InvalidInputError(f"Header: (Partial assignments) has an input with a slot that does not exist, line: {lineNum}")
                        game.setPartialAssignmentSlot(slot)
                    elif(data.Practices.getPracticeByIdentifier(element) != None): # If its a practice
                        practice = data.Practices.getPracticeByIdentifier(element)
                        slot = data.PracticeSlots.getPracticeSlotByDayAndTime(slotDay, slotTime)
                        if (slot == None): raise data.InvalidInputError(f"Header: (Partial assignments) has an input with a slot that does not exist, line: {lineNum}")
                        practice.setPartialAssignmentSlot(slot)
                    else:
                        raise data.InvalidInputError(f"Header: (Partial assignments) has an input with a game/practice that does not exist, line: {lineNum}")
    except data.InvalidInputError as e:
        print(f"Caught Invalid Input Error: {e}")
        sys.exit()

    # add incompatibilities between games and practices of the same teams
    for game in data.Games.getGames():
        if isinstance(game, data.Game):
            for practice in data.Practices.getPractices():
                if isinstance(practice, data.Practice):
                    if practice.getDivision() == None: # Not all practices have division labels. If none that meas that practice is used by all divisions
                        if (game.getOrganization() == practice.getOrganization() and game.getAgeGroup() == practice.getAgeGroup()):
                            game.addIncompatibility(practice)
                            practice.addIncompatibility(game)
                    else:
                        if (game.getOrganization() == practice.getOrganization() and game.getAgeGroup() == practice.getAgeGroup() and game.getDivision() == practice.getDivision()):
                            game.addIncompatibility(practice)
                            practice.addIncompatibility(game)

    # Parse all of the weights and penalties from the command line
    try:
        if not all(item.isdigit() for item in commandLineInputs[1:]): raise data.InvalidInputError(f"Command line contains parameters that are not integers")
        data.WeightsAndPenalties.setMinFilledWeight(commandLineInputs[1])
        data.WeightsAndPenalties.setPrefWeight(commandLineInputs[2])
        data.WeightsAndPenalties.setPairWeight(commandLineInputs[3])
        data.WeightsAndPenalties.setSecDiffWeight(commandLineInputs[4])
        data.WeightsAndPenalties.setGameMinPen(commandLineInputs[5])
        data.WeightsAndPenalties.setPracticeMinPen(commandLineInputs[6])
        data.WeightsAndPenalties.setNotPairedPen(commandLineInputs[7])
        data.WeightsAndPenalties.setSectionPen(commandLineInputs[8])
    except data.InvalidInputError as e:
        print(f"Caught Invalid Input Error: {e}")
        sys.exit()

# run the parser
parser(sys.argv)

# Prints for testing
print(f"Game Slots: {data.GameSlots.getGameSlots()}\n Practice Slots: {data.PracticeSlots.getPracticeSlots()}\n Games: {data.Games.getGames()}\n Practices: {data.Practices.getPractices()}")

print("Not Compatible: ")
for game in data.Games.getGames():
    if isinstance(game, data.Game):
        print(game.getIdentifier(), ":", game.getIncompatibility())
for practice in data.Practices.getPractices():
    if isinstance(practice, data.Practice):
        print(practice.getIdentifier(), ":",practice.getIncompatibility())

print("Unwanted: ")
for game in data.Games.getGames():
    if isinstance(game, data.Game):
        print(game.getIdentifier(), ":", game.getUnwantedSlots())
for practice in data.Practices.getPractices():
    if isinstance(practice, data.Practice):
        print(practice.getIdentifier(), ":",practice.getUnwantedSlots())

print("Preferences: ")
for game in data.Games.getGames():
    if isinstance(game, data.Game):
        print(game.getIdentifier(), ":", game.getPreferenceSlots())
for practice in data.Practices.getPractices():
    if isinstance(practice, data.Practice):
        print(practice.getIdentifier(), ":",practice.getPreferenceSlots())

print("Pair: ")
for game in data.Games.getGames():
    if isinstance(game, data.Game):
        print(game.getIdentifier(), ":", game.getPairs())
for practice in data.Practices.getPractices():
    if isinstance(practice, data.Practice):
        print(practice.getIdentifier(), ":",practice.getPairs())

print("Partial Assignment: ")
for game in data.Games.getGames():
    if isinstance(game, data.Game):
        print(game.getIdentifier(), ":", game.getPartialAssignmentSlot())
for practice in data.Practices.getPractices():
    if isinstance(practice, data.Practice):
        print(practice.getIdentifier(), ":",practice.getPartialAssignmentSlot())

print("Weights and Penalties:")
print(data.WeightsAndPenalties.getMinFilledWeight())
print(data.WeightsAndPenalties.getPrefWeight())
print(data.WeightsAndPenalties.getPairWeight())
print(data.WeightsAndPenalties.getSecDiffWeight())
print(data.WeightsAndPenalties.getGameMinPen())
print(data.WeightsAndPenalties.getPracticeMinPen())
print(data.WeightsAndPenalties.getNotPairedPen())
print(data.WeightsAndPenalties.getSectionPen())
