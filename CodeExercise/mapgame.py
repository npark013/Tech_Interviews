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
roomList = [] #used to convert xml string to list
roomVisitedFlags = [] 
roomNames = []
giantLookUpTable = pd.DataFrame()

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
    global roomNames
    attr = 'roomName'

    for room in root:
        tempName = room.attrib['name']

        rmstr += tempName
        rmstr += ','

    roomList = Convert(rmstr)
    roomList.pop()

    addToLUT(roomList, attr)

    return 

def createroomVisitedFlags():
    global roomVisitedFlags
    global roomList
    rows = len(roomList)
    cols = 2

    #roomVisitedFlags = [[[0 for i in range(cols)] for j in range(rows)]]

    # for i in range(rows):
    #     for j in range(cols):
    #         roomVisitedFlags[i][0] = roomList[i]

    #roomVisitedFlags = np.concatenate((np.zeros((len(roomList),1), dtype=int), roomList), axis=1)

    #roomVisitedFlags = np.array(roomList).reshape(1, 2)

    #roomVisitedFlags = roomList.reshape(rows, cols)
  
    # for i in range(rows):
    #     roomVisitedFlags[i][0] = roomList[i] 

    return

def grabWorldObjects():
    
    return

def createRoomVisitedEmpty():
    
    #print(np.zeros((len(roomList),1), dtype=int))

    return


def createItemFlagsEmpty():
    
    return

def createItemChecklist():
    
    return

###################### M A I N  C O D E ######################

## fills roomList with list of all rooms from map
grabRoomIds(roomString)
roomString = ''
grabRoomNames(roomString)
roomString = ''

print(giantLookUpTable)



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



