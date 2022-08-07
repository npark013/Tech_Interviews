import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import bs4 as bs

nodeTree = ET.parse('map.xml')

root = nodeTree.getroot()

##testing##
    #root.tag and root.tag[0:3] = "map"
    #root.tag[0:2] = "ma"
    #root.tag[0] and root.tag[0:1] = "m"
    #root.tag[1] = "a"

print (root.tag)

################## V A R S ################

roomString = '' #to extract xml id data
giantLookUpTable = pd.DataFrame()
roomList = [] #used to convert xml string to list
# roomNames = []
# roomsNorth = []
# roomsNorth = []
# roomsEast = []
# roomsSouth = []
# roomsWest = []
# worldObjects = []
roomVisitedChecklist = [] 
directionVisitedN = []
directionVisitedE = []
directionVisitedS = []
directionVisitedW = []
roomItemChecklist = []

################## D E F S ################

def Convert(string):
    li = list(string.split(","))
    return li

#adds the next column to giantLookUpTable
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

def createroomVisitedChecklist():
    global roomVisitedChecklist
    global roomList
    attr = 'roomsVisited'
    rows = len(roomList)
    emptyArray = [0]*rows

    roomVisitedChecklist = emptyArray

    addToLUT(roomVisitedChecklist, attr)

    return

def createDirectionVisitedNorth():
    global directionVisitedN
    global roomList
    attr = 'directN'
    rows = len(roomList)
    emptyArray = [0]*rows

    directionVisitedN = emptyArray

    addToLUT(directionVisitedN, attr)
    return
    
def createDirectionVisitedEast():
    global directionVisitedE
    global roomList
    attr = 'directE'
    rows = len(roomList)
    emptyArray = [0]*rows

    directionVisitedE = emptyArray

    addToLUT(directionVisitedE, attr)
    return

def createDirectionVisitedSouth():
    global directionVisitedS
    global roomList
    attr = 'directS'
    rows = len(roomList)
    emptyArray = [0]*rows

    directionVisitedS = emptyArray

    addToLUT(directionVisitedS, attr)
    return

def createDirectionVisitedWest():
    global directionVisitedW
    global roomList
    attr = 'directW'
    rows = len(roomList)
    emptyArray = [0]*rows

    directionVisitedW = emptyArray

    addToLUT(directionVisitedW, attr)
    return

def createItemChecklist():
    global roomItemChecklist
    global roomList
    attr = 'itemChecklist'
    rows = len(roomList)
    emptyArray = [0]*rows

    roomItemChecklist = emptyArray

    addToLUT(roomItemChecklist, attr)
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
createItemChecklist()

print(giantLookUpTable)

## maze navigation loop goes here






##############################################################
##testing##
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



