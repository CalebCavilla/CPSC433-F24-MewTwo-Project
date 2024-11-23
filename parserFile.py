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
    fileInput = commandLineInputs[0]

    
    currentHeader = None
    headers = ["Name:", "Game slots:", "Practice slots:", "Games:", "Practices:", "Not compatible:", "Unwanted:", "Preferences:", "Pair:", "Partial assignments:"]

    try:
        with open(fileInput, 'r') as file:
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
                    if (len(words) != 4): 
                        raise data.InvalidInputError(
                            f"Header: (Game Slots) has an input with incorrect number of parameters, line: {lineNum}"
                        )
                    if (words[0] not in ["MO", "TU", "FR"]): 
                        raise data.InvalidInputError(
                            f"Header: (Game Slots) has an input with invalid day label, line: {lineNum}"
                        )
                    if not is_time_in_range(words[1]): 
                        raise data.InvalidInputError(
                            f"Header: (Game Slots) has an input with invalid time label, line: {lineNum}"
                        )
                    if not words[2].isdigit(): 
                        raise data.InvalidInputError(
                            f"Header: (Game Slots) has an input with invalid gameMax, line: {lineNum}"
                        )
                    if not words[3].isdigit(): 
                        raise data.InvalidInputError(
                            f"Header: (Game Slots) has an input with invalid gameMin, line: {lineNum}"
                        )

                    # assign valid inputs
                    day, time, gameMax, gameMin = words[0], words[1], int(words[2]), int(words[3])
                    gameSlot = data.GameSlot(day, time, gameMax, gameMin)
                    data.GameSlots.addGameSlot(gameSlot)

                elif currentHeader == "Practice slots":
                    words = [word.strip() for word in strippedLine.split(",")] # get the individual words out of the line

                    # Invalid Input checking
                    if (len(words) != 4): 
                        raise data.InvalidInputError(
                            f"Header: (Practice Slots) has an input with incorrect number of parameters, line: {lineNum}"
                            )
                    if (words[0] not in ["MO", "TU", "FR"]): 
                        raise data.InvalidInputError(
                            f"Header: (Practice Slots) has an input with invalid day label, line: {lineNum}"
                            )
                    if not is_time_in_range(words[1]): 
                        raise data.InvalidInputError(
                            f"Header: (Practice Slots) has an input with invalid time label, line: {lineNum}"
                            )
                    if not words[2].isdigit(): 
                        raise data.InvalidInputError(
                            f"Header: (Practice Slots) has an input with invalid gameMax, line: {lineNum}"
                            )
                    if not words[3].isdigit(): 
                        raise data.InvalidInputError(
                            f"Header: (Practice Slots) has an input with invalid gameMin, line: {lineNum}"
                            )
                    
                    # assign valid inputs
                    day, time, practiceMax, practiceMin = words[0], words[1], int(words[2]), int(words[3])
                    practiceSlot = data.PracticeSlot(day, time, practiceMax, practiceMin)
                    data.PracticeSlots.addPracticeSlot(practiceSlot)

                elif currentHeader == "Games":
                    words = strippedLine.split()

                    if (len(words) != 4): 
                        raise data.InvalidInputError(
                            f"Header: (Games) has an input with incorrect number of parameters, line: {lineNum}"
                        )
                    # assign valid inputs
                    # !!! Gonna need to optimize how games are added in the addGame method
                    game = data.Game(strippedLine)
                    data.Games.addGame(game)

                elif currentHeader == "Practices":
                    words = strippedLine.split()

                    if (len(words) != 4 and len(words) != 6): 
                        raise data.InvalidInputError(
                            f"Header: (Practices) has an input with incorrect number of parameters, line: {lineNum}"
                        )
                    # assign valid inputs
                    # !!! Gonna need to optimize how practices are added in the addPractice method
                    practice = data.Practice(strippedLine)
                    data.Practices.addPractice(practice)

                elif currentHeader == "Not compatible":
                    words = [word.strip() for word in strippedLine.split(",")] # get the individual words out of the line
                    if (len(words) != 2): 
                        raise data.InvalidInputError(
                            f"Header: (Not compatible) has an input with incorrect number of parameters, line: {lineNum}"
                        )

                    element1, element2 = words[0], words[1]
                    # determine if inputs for preferences are games or practices or invalid inputs
                    if ("OPN" in words[0] or "PRC" in words[0]):
                        element1 = data.Practices.getPracticeByIdentifier(words[0])
                    else:
                        element1 = data.Games.getGameByIdentifier(words[0])

                    if ("OPN" in words[1] or "PRC" in words[1]):
                        element2 = data.Practices.getPracticeByIdentifier(words[1])
                    else:
                        element2 = data.Games.getGameByIdentifier(words[1])

                    if (not element1 or not element2):
                        raise data.InvalidInputError(
                            f"Header: (Incompatible) has an input with a game/practice that does not exist, line: {lineNum}"
                        )
                    else:
                        # verification of element existence and types are complete
                        # so adding incompatibilities is certain
                        element1.addIncompatibility(element2)
                        element2.addIncompatibility(element1)

                elif currentHeader == "Unwanted":
                    words = [word.strip() for word in strippedLine.split(",")] # get the individual words out of the line
                    if (len(words) != 3): 
                        raise data.InvalidInputError(
                            f"Header: (Unwanted) has an input with incorrect number of parameters, line: {lineNum}"
                        )

                    slotDay, slotTime = words[1], words[2]

                    # depending on game or practice, initialize appropriate element and slot of appropriate type
                    if ("OPN" in words[0] or "PRC" in words[0]):
                        element = data.Practices.getPracticeByIdentifier(words[0])
                        slot = data.PracticeSlots.getPracticeSlotByDayAndTime(slotDay, slotTime)
                    else:
                        element = data.Games.getGameByIdentifier(words[0])
                        slot = data.GameSlots.getGameSlotByDayAndTime(slotDay, slotTime)

                    if(not element):
                        raise data.InvalidInputError(f"Header: (Unwanted) has an input with a game/practice that does not exist, line: {lineNum}")
                    if (not slot): 
                        raise data.InvalidInputError(f"Header: (Unwanted) has an input with a slot that does not exist, line: {lineNum}")

                    element.addUnwantedSlot(slot)

                elif currentHeader == "Preferences":
                    words = [word.strip() for word in strippedLine.split(",")] # get the individual words out of the line
                    if (len(words) != 4): 
                        raise data.InvalidInputError(f"Header: (Preferences) has an input with incorrect number of parameters, line: {lineNum}")
                    
                    slotDay, slotTime, preferenceValue = words[0], words[1], words[3]
                    # depending on game or practice, initialize appropriate element and slot of appropriate type
                    if ("OPN" in words[2] or "PRC" in words[2]):
                        element = data.Practices.getPracticeByIdentifier(words[2])
                        slot = data.PracticeSlots.getPracticeSlotByDayAndTime(slotDay, slotTime)
                    else:
                        element = data.Games.getGameByIdentifier(words[2])
                        slot = data.GameSlots.getGameSlotByDayAndTime(slotDay, slotTime)

                    # validation for preferences; game must exist even if slot does not
                    if (not slot): 
                        print(f"WARNING, Header: (Preferences) has an input with a slot that does not exist, line: {lineNum}"); continue
                    elif (not element):
                        print(data.InvalidInputError(f"WARNING Header: (Preferences) has an input with a game/practice that does not exist, line: {lineNum}")); continue
                    
                    element.addPreferenceSlot(slot, preferenceValue)

                elif currentHeader == "Pair":
                    words = [word.strip() for word in strippedLine.split(",")] # get the individual words out of the line
                    if (len(words) != 2):
                        raise data.InvalidInputError(f"Header: (Pair) has an input with incorrect number of parameters, line: {lineNum}")
                    
                    element1, element2 = words[0], words[1]
                    # determine if inputs for preferences are games or practices or invalid inputs
                    if ("OPN" in words[0] or "PRC" in words[0]):
                        element1 = data.Practices.getPracticeByIdentifier(words[0])
                    else:
                        element1 = data.Games.getGameByIdentifier(words[0])

                    if ("OPN" in words[1] or "PRC" in words[1]):
                        element2 = data.Practices.getPracticeByIdentifier(words[1])
                    else:
                        element2 = data.Games.getGameByIdentifier(words[1])

                    if (not element1 or not element2):
                        raise data.InvalidInputError(
                            f"Header: (Pair) has an input with a game/practice that does not exist, line: {lineNum}"
                        )
                    else:
                        # verification of element existence and types are complete so adding pairs is certain
                        element1.addPair(element2)
                        element2.addPair(element1)

                elif currentHeader == "Partial assignments":
                    words = [word.strip() for word in strippedLine.split(",")] # get the individual words out of the line
                    if (len(words) != 3): 
                        raise data.InvalidInputError(f"Header: (Partial assignments) has an input with incorrect number of parameters, line: {lineNum}")
                    
                    slotDay, slotTime = words[1], words[2] 
                    # set appropriate game/practice element and slot
                    if ("OPN" in words[0] or "PRC" in words[0]):
                        element = data.Practices.getPracticeByIdentifier(words[0])
                        slot = data.PracticeSlots.getPracticeSlotByDayAndTime(slotDay, slotTime)
                    else:
                        element = data.Games.getGameByIdentifier(words[0])
                        slot = data.GameSlots.getGameSlotByDayAndTime(slotDay, slotTime)

                    if(not element):
                        raise data.InvalidInputError(f"Header: (Partial assignments) has an input with a game/practice that does not exist, line: {lineNum}")
                    if (not slot): 
                        raise data.InvalidInputError(f"Header: (Partial assignments) has an input with a slot that does not exist, line: {lineNum}")

                    element.setPartialAssignmentSlot(slot)
                    
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
        print(f"Caught Invalid Weight and penalty read: {e}")
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

# print("Weights and Penalties:")
# print(data.WeightsAndPenalties.getMinFilledWeight())
# print(data.WeightsAndPenalties.getPrefWeight())
# print(data.WeightsAndPenalties.getPairWeight())
# print(data.WeightsAndPenalties.getSecDiffWeight())
# print(data.WeightsAndPenalties.getGameMinPen())
# print(data.WeightsAndPenalties.getPracticeMinPen())
# print(data.WeightsAndPenalties.getNotPairedPen())
# print(data.WeightsAndPenalties.getSectionPen())
