## Code Exercise: A-Maze-ingly Retro Route Puzzle
## Written by Noelle Parker, August 2022
## 
## This python program parses data from a map.xml file, creates a model of the 
## map via a dataframe, and then output a valid route through the map's maze. 
## The file also uses a scenario.txt file to catalog which room is the starting 
## room and which items are necessary to grab along the route. 

import re
import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import bs4 as bs

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

# ## makes empty bool column for data frame
# def createItemChecklist():
#     global roomItemChecklist
#     global roomList
#     attr = 'itemChecklist'
#     rows = len(roomList)

#     emptyArray = [0]*rows
#     roomItemChecklist = emptyArray
#     addToLUT(roomItemChecklist, attr)
#     return

#
def updateRoomVisCheck():
    global giantLookUpTable
    global currentRoom

    giantLookUpTable.at[currentRoom,"roomsVisited"] = '1'
    return
    
#
def updateDirVisN():
    global giantLookUpTable
    global currentRoom

    giantLookUpTable.at[currentRoom,"goneN"] = '1'
    return

#
def updateDirVisE():
    global giantLookUpTable
    global currentRoom

    giantLookUpTable.at[currentRoom,"goneE"] = '1'
    return

#
def updateDirVisS():
    global giantLookUpTable
    global currentRoom

    giantLookUpTable.at[currentRoom,"goneS"] = '1'
    return

#
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

    if (roomObject != '0' and roomObject not in itemsFound):
        itemsFound.append(roomObject)
        giantLookUpTable.at[currentRoom,"roomItems"] = '0'

        print('Picked up ' + roomObject + ' in ' + currentRoom + '.\n')

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

    

    if not histN and currN != '0':
        if currN != historyLog[-1]:
            direction = "North"
            print('Going ' + direction)
            historyLog.append(currentRoom)
            giantLookUpTable.at[currentRoom, "goneN"] = '1'
            return currN
        else:
            backTrack = "North"
            giantLookUpTable.at[currentRoom, "goneN"] = '1'
    
    elif not histE and currE != '0':
        if currE != historyLog[-1]:
            direction = "East"
            print('Going ' + direction)
            historyLog.append(currentRoom)
            giantLookUpTable.at[currentRoom, "goneE"] = '1'
            return currE
        else:
            backTrack = "East"
            giantLookUpTable.at[currentRoom, "goneE"] = '1'

    
    elif not histS and currS != '0':
        if currS != historyLog[-1]:
            direction = "South"
            print('Going ' + direction)
            historyLog.append(currentRoom)
            giantLookUpTable.at[currentRoom, "goneS"] = '1'
            return currS
        else:
            backTrack = "South"
            giantLookUpTable.at[currentRoom, "goneS"] = '1'

    elif not histW and currW != '0':
        if currW != historyLog[-1]:
            direction = "West"
            print('Going ' + direction)
            historyLog.append(currentRoom)
            giantLookUpTable.at[currentRoom, "goneW"] = '1'
            return currW
        else:
            backTrack = "West"
            giantLookUpTable.at[currentRoom, "goneW"] = '1'

    else: 
        print ('Going back ' + backTrack)
        return historyLog.pop()


    return


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
#createItemChecklist()

#set index to room-Id must be done after df completion or include index in every additional column
giantLookUpTable.set_index('roomID', inplace=True)
Index = giantLookUpTable.index

## Find out starting room and objects needed for route
readTxtFile(scenarioFile) 
startingRoom = textFileInfo[0]
currentRoom = startingRoom
historyLog.append(startingRoom)
textFileInfo.remove(startingRoom)

## Maze navigation loop
while not allNeededItemsCollected:
    roomSeen = giantLookUpTable.at[currentRoom,"roomsVisited"]

    if not roomSeen: #new room
        updateRoomVisCheck()
        print('In the ' + currentRoom)

        # grab object if there is one 
        updateInventory()

        # check if all world objects have been retrieved
        checkInventory()
        if allNeededItemsCollected:
            break

        # choose new direction 
        currentRoom = evaluateDirection()

        
    elif roomSeen: #old room
        print('In the ' + currentRoom)

        # choose new direction 
        currentRoom = evaluateDirection()


##############################################################
##Testing##

# giantLookUpTable.at[0,"roomID"]
# giantLookUpTable.iat[1,3]
# df.loc[row_indexer,column_indexer]
# df2[df2["E"].isin(["two", "four"])]
#Direction my need to be saved in a history too unless historylog logs direction

# print(giantLookUpTable.to_string())

# print(giantLookUpTable)
# print('\n')
# print(Index)
# print('\n')
# print(textFileInfo)

# Index = giantLookUpTable.index
# for room in Index:
#     print(giantLookUpTable.at[room,"roomName"])

# print('\nAll info about the foothills:')
# print(giantLookUpTable.loc['foothills',:])

# print('\nNorth of the Kitchen is: ' + giantLookUpTable.at['kitchen','N'])


    #print (root.tag)

    #root.tag and root.tag[0:3] = "map"
    #root.tag[0:2] = "ma"
    #root.tag[0] and root.tag[0:1] = "m"
    #root.tag[1] = "a"

    # #print(roomList)
    # print (room.attrib) #prints all <room> properties
            #print (room.attrib['id']) #prints <room> 'id' property

    # #error happens if attribute not there
    # try: 
    #     print ("North: " + room.attrib['north'])
    # except:
    #     pass
    # try:
    #     print ("East: " + room.attrib['east'])
    # except:
    #     pass
    # try:
    #     print ("South: " + room.attrib['south'])
    # except:
    #     pass
    # try:
    #     print ("West: " + room.attrib['west'])
    # except:
    #     pass


    # #prints object in room if there is one
    # for item in room:
    #     print (item.attrib['name'])


    # print(room.find('object').text) #prints "None"

    #giantLookUpTable = np.array(roomList)



