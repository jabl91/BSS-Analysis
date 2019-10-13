
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
from BikeStationCDF import BikeStationCDF
from NvMAccelerator import NvMAccelerator

import numpy as np

## Provide the class description


class BikeStation:

    # Constants
    C_STATION_ID_ERROR = '-1'
    C_MESSAGES = False
    C_THRESH_RELOC_ACTION = 0.10

    # attributes
    stationCDFDepartures = None
    stationCDFArrivals = None
    relocationsCounter = 0

    backupInitialBikes = 0
    backupInitialDocks = 0

    ## This is the constructor method for the BikeStation method
    def __init__(
            self,
            stationInitialId,
            numberInitialBikes=10,
            numberInitialDocks=20):
        self.numberOfDocks = numberInitialDocks
        self.backupInitialDocks = numberInitialDocks
        self.numberOfBikes = numberInitialBikes
        self.backupInitialBikes = numberInitialBikes
        self.stationId = str(stationInitialId)

        try:
            UnpickledData =\
                NvMAccelerator.pickled_items(
                    './test/' +
                    'CDFStation' + self.stationId + '.pkl')

            for i, myData in enumerate(UnpickledData):
                # print(myData[0])
                # print(myData[1])
                self.stationCDFDepartures = myData[0]
                self.stationCDFArrivals = myData[1]
                break

            # print(self.stationCDFDepartures.numTripsInDay)
            # print(self.stationCDFArrivals.numTripsInDay)
            if(self.C_MESSAGES is True):
                print(
                    '####CDF Information for Station####: ' +
                    self.stationId +
                    '\nSuccesfull\n\n')
        except:
            try:
                self.stationCDFDepartures = \
                    BikeStationCDF(stationInitialId, departure=True)
                self.stationCDFArrivals = \
                    BikeStationCDF(stationInitialId, departure=False)
                NvMAccelerator.save_object(
                    [self.stationCDFDepartures, self.stationCDFArrivals],
                    './test/' + 'CDFStation' + self.stationId + '.pkl')
                print(
                    '####CDF Information for Station####: ' +
                    self.stationId +
                    '\nSuccesfull\n\n')
            except:
                print('No CDF Information for Station: ' + self.stationId)

    ## This is a method to increment the number of available
    # bikes in the station
    def pushBike(self, relocWeight=50):
        returnValue = False
        self.relocationEvent(relocWeight * 0.01)
        if((self.numberOfDocks - self.numberOfBikes) > 0):
            self.numberOfBikes = self.numberOfBikes + 1
            returnValue = True

        return returnValue

    ## This is a method to remove the number of available
    # bikes in the station
    def removeBike(self, relocWeight=50):
        returnValue = False
        self.relocationEvent(relocWeight * 0.01)
        if(self.numberOfBikes > 0):
            self.numberOfBikes = self.numberOfBikes - 1
            returnValue = True

        return returnValue

    ## This is a method to return the number of available bikes for
    # bike station
    def availableBikes(self):
        return self.numberOfBikes

    def relocationEvent(self, cur_RebalPerc):
        if((self.numberOfBikes <=
                int(
                    (self.C_THRESH_RELOC_ACTION) *
                    self.numberOfDocks)) |
            (self.numberOfBikes >=
                int((1 - self.C_THRESH_RELOC_ACTION) *
                    self.numberOfDocks))):
            # print("Camioncito de relocacion")
            # print("Dejando la estacion al " +
            # str(cur_RebalPerc) + "%")
            self.numberOfBikes = \
                int(
                    cur_RebalPerc *
                    self.numberOfDocks)
            self.relocationsCounter += 1

    ## This is a method to return the number bike station id
    #
    def getStationId(self):
        return self.stationId

    def getStationStats(self):
        return [self.relocationsCounter]

    ## This method returns a np.array with the timestamps of the
    # trips that occured within a single day.
    # Column [0] Timestamp of the trips
    # Column [1] If value is equal to 1 then it is an arrival
    # if value is equal to 0 then it is a departure
    def getTripsOnWeekday(self, wkday):
        if(self.stationCDFDepartures is not None and
                self.stationCDFArrivals is not None):
                myDepartures = \
                    self.stationCDFDepartures.getCDFTripsPerDay(wkday)
                myArrivals = \
                    self.stationCDFArrivals.getCDFTripsPerDay(wkday)

                dep_mat = np.c_[
                    np.array(myDepartures), np.zeros(len(myDepartures))]

                arri_mat = np.c_[
                    np.array(myArrivals), np.ones(len(myArrivals))]

                myTrips = np.r_[arri_mat, dep_mat]

                return myTrips[myTrips[:, 0].argsort()]

        else:
            return []

    def resetBikeStation(self):
        self.relocationsCounter = 0
        self.numberOfDocks = self.backupInitialDocks
        self.numberOfBikes = self.backupInitialBikes


## Provide the class description
#
class BikeStationNetwork:

    # constants
    C_DEFAULT_NUM_DOCKS = 20
    C_RELATION_DOCKS_BIKES = 2
    C_ARRIVALS_IDX = 1.0
    C_DEPARTURES_IDX = 0.0

    C_NUMBER_OF_TRIPS = 1

    # attributes
    StationsOnNetwork = []
    DayItinerary = []

    ## This is the constructor method for the BikeStation method
    def __init__(self, NumberOfDocks=20):

        StationsOnNetworkClass = StationInfoClass()
        self.StationsOnNetwork = \
            StationsOnNetworkClass.getBikeStation2EdgeDict()

        self.BikeStationsDict = {}
        for Id in \
                list(self.StationsOnNetwork.keys()):

            self.BikeStationsDict[str(Id)] = BikeStation(
                Id,
                int(NumberOfDocks * 0.50),
                NumberOfDocks)

        self.BikeStationDocks = []

    ## This is a method to return object to the respective Bike station
    # based on bike station Id
    def getBikeStationObject(self, Id):
        if(self.BikeStationsDict.get(str(Id), None) is not None):
            return self.BikeStationsDict.get(str(Id), None)
        else:
            print('Bike Station Id: ' + str(Id) + ' is not loaded.')
            raise

    def getAllStationOnNetwork(self):
        # return [id for [id, _] in self.StationsOnNetwork]
        return list(self.StationsOnNetwork.keys())

    def getDayItinerary(self, wkday):
        self.DayItinerary = []
        AllStationsIds = self.getAllStationOnNetwork()

        for station in AllStationsIds:
            currentBikeStation =\
                self.getBikeStationObject(station)

            for i in range(self.C_NUMBER_OF_TRIPS):
                BikeStationTrips = \
                    currentBikeStation.getTripsOnWeekday(wkday)

                stationId = \
                    np.ones(len(BikeStationTrips)) * int(station)

                Destination_Bool = \
                    BikeStationTrips[:, 1] == \
                    BikeStationNetwork.C_DEPARTURES_IDX

                DestinationInfoValues =\
                    currentBikeStation\
                    .stationCDFDepartures\
                    .getStationDestination(
                        wkday,
                        len(BikeStationTrips[Destination_Bool]))

                DestinationInfo = np.ones(len(BikeStationTrips)) * -1

                DestinationInfo[Destination_Bool] =\
                    DestinationInfoValues

                self.DayItinerary.append(
                    np.c_[BikeStationTrips, stationId, DestinationInfo])

        return self.DayItinerary

    def resetNetwork(self):
        for Id in \
                list(self.StationsOnNetwork.keys()):
            self.getBikeStationObject(Id).resetBikeStation()

# myBikeNetwork = BikeStationNetwork()
# currentBikeStation = myBikeNetwork.getBikeStationObject(34)
# myTrips = currentBikeStation.getTripsOnWeekday(0)
# print(myTrips)
#
# for trip in myTrips:
#     if(trip[1] == BikeStationNetwork.C_ARRIVALS_IDX):
#         print(currentBikeStation.pushBike())
#         print(currentBikeStation.availableBikes())
#     else:
#         print(currentBikeStation.removeBike())
#         print(currentBikeStation.availableBikes())
#
# print('Stations on the network are: ')
# print(myBikeNetwork.getAllStationOnNetwork())
#
# # Retrive the schedule for the current day for the trips to occur
# # myBikeNetwork.getDayItinerary(0)
#
# print(currentBikeStation.getStationStats())
