
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
from EdgesTypesExtractor import EdgeTypesExtractor
from Geometry import GeometryClass

import traci

import math


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

    EdgetoEdgeType = {}
    EdgetoEdgeCenter = {}
    EdgeLinearEquation = {}

    currentTypes = []
    currentEdgeCenters = []
    currentEdgeLinearEquation = []
    VectorPointDirection = []

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

        myEdgeDataExtractor = EdgeTypesExtractor('osm.net.xml')

        self.EdgetoEdgeType = \
            myEdgeDataExtractor.getEdgeTypeDict()
        self.EdgetoEdgeCenter, self.EdgeLinearEquation = \
            myEdgeDataExtractor.getCenterofEdgeDict()
        # print(self.EdgeLinearEquation)

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
        myGeometryAPI = GeometryClass()
        EdgeAngleWeights = []
        self.currentTypes = []
        self.currentEdgeCenters = []
        self.currentEdgeLinearEquation = []

        if traci.route.getEdges(self.myRoute):
            allEdges = traci.route.getEdges(self.myRoute)
            for myEdge in allEdges:
                self.currentTypes.append(
                    self.EdgetoEdgeType[myEdge])
                self.currentEdgeCenters.append(
                    self.EdgetoEdgeCenter[myEdge])
                self.currentEdgeLinearEquation.append(
                    self.EdgeLinearEquation[myEdge])

            print(self.currentTypes)
            print(self.currentEdgeCenters)
            print(self.currentEdgeLinearEquation)

            # This function will calculate the VectorPointDirection
            # this is needed to now the directions of the current
            # route

            self.__findVectorDirection(
                self.currentEdgeCenters, self.currentEdgeLinearEquation)

            lastRouteEdge = len(self.currentEdgeCenters) - 1
            for i, DirectionPoint in enumerate(self.VectorPointDirection):
                EdgeAngleWeights.append(myGeometryAPI.getAngleBetweenVectors(
                    DirectionPoint,
                    self.currentEdgeCenters[lastRouteEdge],
                    self.currentEdgeCenters[i]))

            EdgeAngleWeights = [(1 - i/180.0) for i in EdgeAngleWeights]
            print(EdgeAngleWeights)

            # input('Press Enter to continue...')
            # print(traci.edge.getIDList())

    def __findVectorDirection(self, EdgeCenters, EdgeLinEqs):
        myGeometryAPI = GeometryClass()
        eval_val = myGeometryAPI.getBoundary_Y()
        len_EC = len(EdgeCenters)
        self.VectorPointDirection = []
        for i, EdgeCenter in enumerate(EdgeCenters):
            if((len_EC - 1) > i):
                # Find the closest value to point to find vector direction
                x_rng = \
                        [(eval_val*(-1)) + float(EdgeCenter[0]),
                         eval_val + float(EdgeCenter[0])]

                y_neg = \
                    ((EdgeLinEqs[i][0])*x_rng[0]) + EdgeLinEqs[i][1]

                y_pos = \
                    ((EdgeLinEqs[i][0])*x_rng[1]) + EdgeLinEqs[i][1]

                neg_dist = myGeometryAPI.getDistance(
                    [x_rng[0], y_neg],
                    [float(EdgeCenters[i+1][0]), float(EdgeCenters[i+1][1])])

                pos_dist = myGeometryAPI.getDistance(
                    [x_rng[1], y_pos],
                    [float(EdgeCenters[i+1][0]), float(EdgeCenters[i+1][1])])

                if(neg_dist < pos_dist):
                    distantVectorPoint = [x_rng[0], y_neg]
                else:
                    distantVectorPoint = [x_rng[1], y_pos]

                self.VectorPointDirection.append(distantVectorPoint)
                angleBetweenEdges = \
                    myGeometryAPI.getAngleBetweenVectors(
                        distantVectorPoint,
                        [float(EdgeCenters[i+1][0]),
                         float(EdgeCenters[i+1][1])],
                        [float(EdgeCenter[0]),
                         float(EdgeCenter[1])])
                # print(angleBetweenEdges)

    # def __setattr__(self, name, value):
        # print(bcolors.WARNING + 'ERROR: The attribute ' +
        #      name + ' doesnt exist' + bcolors.ENDC)

    # def __getattribute__(self, name):
        # print(bcolors.WARNING + 'ERROR: The attribute ' +
        #      name + ' doesnt exist' + bcolors.ENDC)


# myRoute = traci.route()

# myRouteAnalysis = RouteAnalysis(myRoute)
# print(myRouteAnalysis)
