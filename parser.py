import sys
import dataClasses as data

commandLineInputs = sys.argv[1:] # get the list of inputs from the command line not including the main file name

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
                if (len(words) != 4): raise data.InvalidInputError(f"Game Slots has an input with incorrect number of parameters, line: {lineNum}")
                day = words[0]
                time = words[1]
                gameMax = int(words[2])
                gameMin = int(words[3])
                gameSlot = data.GameSlot(day, time, gameMax, gameMin)
                data.GameSlots.addGameSlot(gameSlot)
            elif currentHeader == "Practice slots":
                words = [word.strip() for word in strippedLine.split(",")] # get the individual words out of the line
                if (len(words) != 4): raise data.InvalidInputError(f"Practice Slots has an input with incorrect number of parameters, line: {lineNum}")
                day = words[0]
                time = words[1]
                practiceMax = int(words[2])
                practiceMin = int(words[3])
                practiceSlot = data.PracticeSlot(day, time, practiceMax, practiceMin)
                data.PracticeSlots.addPracticeSlot(practiceSlot)
            elif currentHeader == "Games":
                words = strippedLine.split()
                if (len(words) != 4): raise data.InvalidInputError(f"Games has an input with incorrect number of parameters, line: {lineNum}")
                game = data.Game(strippedLine)
                data.Games.addGame(game)
            elif currentHeader == "Practices":
                words = strippedLine.split()
                if (len(words) != 4 and len(words) != 6): raise data.InvalidInputError(f"Practices has an input with incorrect number of parameters, line: {lineNum}")
                practice = data.Practice(strippedLine)
                data.Practices.addPractice(practice)

except data.InvalidInputError as e:
    print(f"Caught Invalid Input Error: {e}")


print(f"Game Slots: {data.GameSlots.getGameSlots()}\n Practice Slots: {data.PracticeSlots.getPracticeSlots()}\n Games: {data.Games.getGames()}\n Practices: {data.Practices.getPractices()}")