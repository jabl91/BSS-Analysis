
## @package BikeStations
#  Add package descrition here.
#
#
# @file    BikeStations.py
# @author  Alberto Briseno
# @date    2019-08-13
# @version $Id$

# import math
# import traci

from StationId2Edge import StationInfoClass

## Provide the class description


class BikeStation:

    # Constants
    C_STATION_ID_ERROR = '-1'

    ## This is the constructor method for the BikeStation method
    def __init__(
            self,
            stationInitialId,
            numberInitialBikes=10,
            numberInitialDocks=20):
        self.numberOfDocks = numberInitialDocks
        self.numberOfBikes = numberInitialBikes
        self.stationId = str(stationInitialId)

    ## This is a method to increment the number of available
    # bikes in the station
    def pushBike(self):
        returnValue = False
        if((self.numberOfDocks - self.numberOfBikes) > 0):
            self.numberOfBikes = self.numberOfBikes + 1
            returnValue = True

        return returnValue

    ## This is a method to remove the number of available
    # bikes in the station
    def removeBike(self):
        returnValue = False
        if(self.numberOfBikes > 0):
            self.numberOfBikes = self.numberOfBikes - 1
            returnValue = True

        return returnValue

    ## This is a method to return the number of available bikes for
    # bike station
    def availableBikes(self):
        return self.numberOfBikes

    ## This is a method to return the number bike station id
    #
    def getStationId(self):
        return self.stationId


## Provide the class description
#
class BikeStationNetwork:

    # constants
    C_DEFAULT_NUM_DOCKS = 15
    C_RELATION_DOCKS_BIKES = 2

    # attributes
    StationsOnNetwork = []

    ## This is the constructor method for the BikeStation method
    def __init__(self):

        StationsOnNetworkClass = StationInfoClass()
        self.StationsOnNetwork = \
            StationsOnNetworkClass.getBikeStation2EdgeDict()

        self.BikeStationsDict = {}
        for Id in \
                list(self.StationsOnNetwork.keys()):

            self.BikeStationsDict[str(Id)] = BikeStation(
                Id,
                int(self.C_DEFAULT_NUM_DOCKS / self.C_RELATION_DOCKS_BIKES),
                self.C_DEFAULT_NUM_DOCKS)

        self.BikeStationDocks = []

    ## This is a method to return object to the respective Bike station
    # based on bike station Id
    def getBikeStationObject(self, Id):
        return self.BikeStationsDict.get(str(Id), BikeStation(-1, 0, 0))

    def getAllStationOnNetwork(self):
        # return [id for [id, _] in self.StationsOnNetwork]
        return list(self.StationsOnNetwork.keys())


myBikeNetwork = BikeStationNetwork()
currentBikeStation = myBikeNetwork.getBikeStationObject(34)
if(currentBikeStation.getStationId() != BikeStation.C_STATION_ID_ERROR):
    for i in range(1, 20):
        print(currentBikeStation.pushBike())
        print(currentBikeStation.availableBikes())
    for i in range(1, 25):
        print(currentBikeStation.removeBike())
        print(currentBikeStation.availableBikes())
else:
    print('BikeStation.py: Station doesn\'t exist\n')
    raise

print('Stations on the network are: ')
print(myBikeNetwork.getAllStationOnNetwork())
