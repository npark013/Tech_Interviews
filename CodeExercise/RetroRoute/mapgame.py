## Code Exercise: A-Maze-ingly Retro Route Puzzle
## Written by Noelle Parker, August 2022
## 
## This python program parses data from a map.xml file, creates a model of the 
## map via a dataframe, and then output a valid route through the map's maze. 
## The file also uses a scenario.txt file to catalog which room is the starting 
## room and which items are necessary to grab along the route. 

import xml.etree.ElementTree as ET
import pandas as pd

nodeTree = ET.parse('map.xml')

root = nodeTree.getroot()    

## Note: Starting room in text file must match format for room 'id' and
## objects in text file must match format for object 'name' with respect to map.xml
scenarioFile = 'scenario.txt' 

################## V A R S ################

giantLookUpTable = pd.DataFrame()
roomString = '' #to extract xml id data
roomList = [] #used to convert xml string to list
roomVisitedChecklist = [] 
directionVisitedN = []
directionVisitedE = []
directionVisitedS = []
directionVisitedW = []
itemsFound = [] #inventory
allNeededItemsCollected = False 
textFileInfo = [] #used to convert txt file to list
startingRoom = ''
currentRoom = '' #state
direction = ''
historyLog = [] #tracking enabled

################## D E F S ################

def Convert(string):
    li = list(string.split(","))
    return li

## textFileInfo populated
def readTxtFile(filename):
    global textFileInfo
    with open(filename) as file:
        lines = file.readlines()
        textFileInfo = [line.rstrip() for line in lines]
    return

## adds the next column to giantLookUpTable
def addToLUT(nextList, attrStr):
    global giantLookUpTable
    tempList = pd.DataFrame(nextList, columns=[attrStr])
    giantLookUpTable = pd.concat([giantLookUpTable, tempList], axis=1)
    return

## extracts room list from map.xml
def grabRoomIds(rmstr):
    global roomList
    attr = 'roomID'
    for room in root:
        tempName = room.attrib['id']
        rmstr += tempName
        rmstr += ','

    roomList = Convert(rmstr)
    roomList.pop()
    addToLUT(roomList, attr)
    return 

## extracts room names from map.xml
def grabRoomNames(rmstr):
    attr = 'roomName'
    for room in root:
        tempName = room.attrib['name']
        rmstr += tempName
        rmstr += ','

    roomList = Convert(rmstr)
    roomList.pop()
    addToLUT(roomList, attr)
    return 

## extracts rooms with Norths from map.xml
def grabNorth(rmstr):
    attr = 'N'
    for room in root:
        try: 
            tempName = room.attrib['north']
        except:
            tempName = '0'
        finally:
            rmstr += tempName
            rmstr += ','

    roomList = Convert(rmstr)
    roomList.pop()
    addToLUT(roomList, attr)
    return

## extracts rooms with Easts from map.xml
def grabEast(rmstr):
    attr = 'E'
    for room in root:
        try: 
            tempName = room.attrib['east']
        except:
            tempName = '0'
        finally:
            rmstr += tempName
            rmstr += ','

    roomList = Convert(rmstr)
    roomList.pop()
    addToLUT(roomList, attr)
    return

## extracts rooms with Souths from map.xml
def grabSouth(rmstr):
    attr = 'S'
    for room in root:
        try: 
            tempName = room.attrib['south']
        except:
            tempName = '0'
        finally:
            rmstr += tempName
            rmstr += ','

    roomList = Convert(rmstr)
    roomList.pop()
    addToLUT(roomList, attr)
    return

## extracts rooms with Wests from map.xml
def grabWest(rmstr):
    attr = 'W'
    for room in root:
        try: 
            tempName = room.attrib['west']
        except:
            tempName = '0'
        finally:
            rmstr += tempName
            rmstr += ','

    roomList = Convert(rmstr)
    roomList.pop()
    addToLUT(roomList, attr)
    return

## extracts room objects from map.xml
def grabWorldObjects(rmstr):
    attr = 'roomItems'
    for room in root:
        try:
            tempName = room.find('object').attrib['name']
        except:
            tempName = '0'
        finally:
            rmstr += tempName
            rmstr += ','

    roomList = Convert(rmstr)
    roomList.pop()
    addToLUT(roomList, attr)
    return

## makes empty bool column for data frame
def createroomVisitedChecklist():
    global roomVisitedChecklist
    global roomList
    attr = 'roomsVisited'
    rows = len(roomList)

    emptyArray = [0]*rows
    roomVisitedChecklist = emptyArray
    addToLUT(roomVisitedChecklist, attr)

    return

## makes empty bool column for data frame
def createDirectionVisitedNorth():
    global directionVisitedN
    global roomList
    attr = 'goneN'
    rows = len(roomList)

    emptyArray = [0]*rows
    directionVisitedN = emptyArray
    addToLUT(directionVisitedN, attr)
    return

## makes empty bool column for data frame
def createDirectionVisitedEast():
    global directionVisitedE
    global roomList
    attr = 'goneE'
    rows = len(roomList)

    emptyArray = [0]*rows
    directionVisitedE = emptyArray
    addToLUT(directionVisitedE, attr)
    return

## makes empty bool column for data frame
def createDirectionVisitedSouth():
    global directionVisitedS
    global roomList
    attr = 'goneS'
    rows = len(roomList)

    emptyArray = [0]*rows
    directionVisitedS = emptyArray
    addToLUT(directionVisitedS, attr)
    return

## makes empty bool column for data frame
def createDirectionVisitedWest():
    global directionVisitedW
    global roomList
    attr = 'goneW'
    rows = len(roomList)

    emptyArray = [0]*rows
    directionVisitedW = emptyArray
    addToLUT(directionVisitedW, attr)
    return

## sets roomsVisited column to 1
def updateRoomVisCheck():
    global giantLookUpTable
    global currentRoom

    giantLookUpTable.at[currentRoom,"roomsVisited"] = '1'
    return
    
## sets goneDir column to 1
def updateDirVisN():
    global giantLookUpTable
    global currentRoom

    giantLookUpTable.at[currentRoom,"goneN"] = '1'
    return

## sets goneDir column to 1
def updateDirVisE():
    global giantLookUpTable
    global currentRoom

    giantLookUpTable.at[currentRoom,"goneE"] = '1'
    return

## sets goneDir column to 1
def updateDirVisS():
    global giantLookUpTable
    global currentRoom

    giantLookUpTable.at[currentRoom,"goneS"] = '1'
    return

## sets goneDir column to 1
def updateDirVisW():
    global giantLookUpTable
    global currentRoom

    giantLookUpTable.at[currentRoom,"goneW"] = '1'
    return

## picks up item in room if present
def updateInventory():
    global giantLookUpTable
    global currentRoom
    roomObject = giantLookUpTable.at[currentRoom,"roomItems"]
    currRoomName = giantLookUpTable.at[currentRoom, "roomName"]

    if (roomObject != '0' and roomObject not in itemsFound):
        itemsFound.append(roomObject)
        giantLookUpTable.at[currentRoom,"roomItems"] = '0'
        print('\nPicked up ' + roomObject + ' in ' + currRoomName + '!\n')
    return

## modifies allNeededItemsCollected if necessary
def checkInventory():
    global allNeededItemsCollected
    global itemsFound
    global textFileInfo

    if set(itemsFound) == set(textFileInfo):
        allNeededItemsCollected = True
    return

# chooses room you will go based on direction/backtracking priority
def evaluateDirection():
    global giantLookUpTable
    global currentRoom
    global historyLog
    global direction
    backTrack = ''

    currN = giantLookUpTable.at[currentRoom, "N"]
    currE = giantLookUpTable.at[currentRoom, "E"]
    currS = giantLookUpTable.at[currentRoom, "S"]
    currW = giantLookUpTable.at[currentRoom, "W"]

    histN = giantLookUpTable.at[currentRoom, "goneN"]
    histE = giantLookUpTable.at[currentRoom, "goneE"]
    histS = giantLookUpTable.at[currentRoom, "goneS"]
    histW = giantLookUpTable.at[currentRoom, "goneW"]

    
    if currN != historyLog[-1]:
        if not histN and currN != '0':
            direction = "North"
            print('Going ' + direction)
            historyLog.append(currentRoom)
            updateDirVisN()
            return currN 
    else:
        backTrack = "North"
        updateDirVisN()
                

    if currE != historyLog[-1]:
        if not histE and currE != '0':
            direction = "East"
            print('Going ' + direction)
            historyLog.append(currentRoom)
            updateDirVisE()
            return currE
    else:
        backTrack = "East"
        updateDirVisE()

    if currS != historyLog[-1]:
        if not histS and currS != '0':
            direction = "South"
            print('Going ' + direction)
            historyLog.append(currentRoom)
            updateDirVisS()
            return currS
    else:
        backTrack = "South"
        updateDirVisS()

    if currW != historyLog[-1]:
        if not histW and currW != '0':
        
            direction = "West"
            print('Going ' + direction)
            historyLog.append(currentRoom)
            updateDirVisW()
            return currW
    else:
        backTrack = "West"
        updateDirVisW()

    print ('Going back ' + backTrack)
    return historyLog.pop()



###################### M A I N  C O D E ######################

## Fill LUT with map info & additional columns
grabRoomIds(roomString)
roomString = ''
grabRoomNames(roomString)
roomString = ''
grabNorth(roomString)
roomString = ''
grabEast(roomString)
roomString = ''
grabSouth(roomString)
roomString = ''
grabWest(roomString)
roomString = ''
grabWorldObjects(roomString)
roomString = ''
createroomVisitedChecklist()
createDirectionVisitedNorth()
createDirectionVisitedEast()
createDirectionVisitedSouth()
createDirectionVisitedWest()

#set index to room-Id must be done after df completion or include index in every additional column
giantLookUpTable.set_index('roomID', inplace=True)

## Find out starting room and objects needed for route
readTxtFile(scenarioFile) 
startingRoom = textFileInfo[0]
currentRoom = startingRoom
historyLog.append(startingRoom)
textFileInfo.remove(startingRoom)

## Maze navigation loop
while not allNeededItemsCollected:
    roomSeen = giantLookUpTable.at[currentRoom,"roomsVisited"]
    currRoomName = giantLookUpTable.at[currentRoom, "roomName"]

    if not roomSeen: #new room
        updateRoomVisCheck()
        print('In the ' + currRoomName)

        # grab object if there is one 
        updateInventory()

        # check if all world objects have been retrieved
        checkInventory()
        if allNeededItemsCollected:
            print ('All items collected!')
            break

        # choose new direction 
        currentRoom = evaluateDirection()

    elif roomSeen: #old room
        print('In the ' + currRoomName)

        # choose new direction 
        currentRoom = evaluateDirection()

##############################################################