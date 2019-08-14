
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


## Provide the class description
#
class BikeStation:

    ## This is the constructor method for the BikeStation method
    def __init__(
            self,
            stationInitialId,
            numberInitialBikes=10,
            numberInitialDocks=20):
        self.numberOfDocks = numberInitialDocks
        self.numberOfBikes = numberInitialBikes
        self.stationId = stationInitialId

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

    ## This is the constructor method for the BikeStation method
    def __init__(self, BikeStationsInfo):
        self.BikeStationsDict = {}
        for Id, BikesNumber, DocksNumber in BikeStationsInfo:
            self.BikeStationsDict[str(Id)] = BikeStation(
                Id, BikesNumber, DocksNumber)

    ## This is a method to return object to the respective Bike station
    # based on bike station Id
    def getBikeStationObject(self, Id):
        return self.BikeStationsDict[str(Id)]


myBikeStations = [[0, 10, 20]]
# Object Creation for BikeStationsNetwork

myBikeNetwork = BikeStationNetwork(myBikeStations)
currentBikeStation = myBikeNetwork.getBikeStationObject(0)
for i in range(1, 20):
    print(currentBikeStation.pushBike())
    print(currentBikeStation.availableBikes())
for i in range(1, 25):
    print(currentBikeStation.removeBike())
    print(currentBikeStation.availableBikes())
