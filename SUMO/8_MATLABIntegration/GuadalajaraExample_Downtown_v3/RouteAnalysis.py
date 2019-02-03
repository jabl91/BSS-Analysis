
# This file contains the required methods to calculate which
# routes are better than others taking into consideration
# the weights table proposed on Mapping cyclists' experiences
# and agent-based modelling of their wayfinding behaviour(Snizek, 2015)
# The analysis is also based in that project Git Repo that is located at
# https://github.com/bsnizek/CopenhagenABM

# @file    RouteAnalysis.py
# @author  Alberto Briseno
# @date    2019-01-21
# @version $Id$

from __future__ import absolute_import
from __future__ import print_function

# import os
# import sys
# import optparse
# import random

from myPythonDependencies.myConstants import myConstants

import traci


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class RouteAnalysis:

    myRoute = ''
    myDecision = ''
    AllLanes = []
    AllEdges = []
    LaneToEdge = {}

    def __init__(self):
        self.myRoute = 'myRoute'
        self.myDecision = 'CurrentRoute'
        self.AllLanes = traci.lane.getIDList()
        self.AllEdges = traci.edge.getIDList()

        for myLane in self.AllLanes:
            # self.LaneToEdge.append(traci.lane.getEdgeID(myLane))
            self.LaneToEdge[myLane] = traci.lane.getEdgeID(myLane)

        # print(self.LaneToEdge[self.AllLanes[0]])
        # input('Press Enter to continue...')

    def __str__(self):
        return (bcolors.OKBLUE +
                '\nRouteAnalysis Class -- Description\n'
                'This class contains the required methods to calculate which\n'
                'routes are better than others taking into consideration\n'
                'the weights table proposed on Mapping cyclists experiences\n'
                'and agent-based modelling of their wayfinding behaviour\n'
                '(Snizek, 2015)\n' +
                bcolors.ENDC)

    def setCurrentRoute(self, myLocalRoute):
        self.myRoute = myLocalRoute

    def getCurrentRoute(self):
        return self.myRoute

    def getAllEdges(self):
        return traci.route.getEdges(self.myRoute)

    def convertVehicleLane2VehicleEdge(self, myLocalLane):
        return self.LaneToEdge[myLocalLane]

    def setTestMode(self):
        if traci.route.getEdges(self.myRoute):
            allEdges = traci.route.getEdges(self.myRoute)
            firstEdge = allEdges[0]
            # print(traci.edge.getIDList())

    # def __setattr__(self, name, value):
        # print(bcolors.WARNING + 'ERROR: The attribute ' +
        #      name + ' doesnt exist' + bcolors.ENDC)

    # def __getattribute__(self, name):
        # print(bcolors.WARNING + 'ERROR: The attribute ' +
        #      name + ' doesnt exist' + bcolors.ENDC)


# myRoute = traci.route()

# myRouteAnalysis = RouteAnalysis(myRoute)
# print(myRouteAnalysis)
