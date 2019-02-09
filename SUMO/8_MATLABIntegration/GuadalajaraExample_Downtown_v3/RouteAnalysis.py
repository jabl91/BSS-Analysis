
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

    Route_Edges = []

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

        self.myEdgeDataExtractor = EdgeTypesExtractor('osm.net.xml')

        self.EdgetoEdgeType = \
            self.myEdgeDataExtractor.getEdgeTypeDict()
        self.EdgetoEdgeCenter, self.EdgeLinearEquation = \
            self.myEdgeDataExtractor.getCenterofEdgeDict()
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
        self.getAllRoadsinRoute()

    def getCurrentRoute(self):
        return self.myRoute

    def getAllEdges(self):
        return traci.route.getEdges(self.myRoute)

    def convertVehicleLane2VehicleEdge(self, myLocalLane):
        return self.LaneToEdge[myLocalLane]

    # def evaluateAllRoadsinRoute(self):

    def getAllRoadsinRoute(self):
        self.currentTypes = []
        self.currentEdgeCenters = []
        self.currentEdgeLinearEquation = []
        self.Route_Edges = []

        if traci.route.getEdges(self.myRoute):
            self.Route_Edges = traci.route.getEdges(self.myRoute)
            # print(allEdges)
            for myEdge in self.Route_Edges:
                self.currentTypes.append(
                    self.EdgetoEdgeType[myEdge])
                self.currentEdgeCenters.append(
                    self.EdgetoEdgeCenter[myEdge])
                self.currentEdgeLinearEquation.append(
                    self.EdgeLinearEquation[myEdge])

    def getAngleEdgeWeight(self,
                           EdgeCenters,
                           EdgeLinearEq,
                           Destination,
                           NotARoute=False,
                           BaseEdgeIdx=0):
        myGeometryAPI = GeometryClass()
        EdgeAngleWeights = []

        # This function will calculate the VectorPointDirection
        # this is needed to now the directions of the current
        # route

        VectorPointDirection = self.__findVectorDirection(
            EdgeCenters, EdgeLinearEq, NotARoute, BaseEdgeIdx)

        for i, DirectionPoint in enumerate(VectorPointDirection):
            EdgeAngleWeights.append(myGeometryAPI.getAngleBetweenVectors(
                DirectionPoint,
                Destination,
                EdgeCenters[i]))

        EdgeAngleWeights = [(1 - i/180.0) for i in EdgeAngleWeights]

        # print(EdgeAngleWeights)
        return EdgeAngleWeights

        # input('Press Enter to continue...')
        # print(traci.edge.getIDList())

    def processDecisionWeightsForEdges(
            self,
            EdgeCenters,
            EdgeLinearEqs,
            Destination,
            NotARoute=False,
            BaseEdgeIdx=0):

            AngleEdgeWeights = []
            AngleEdgeWeights = (self.getAngleEdgeWeight(
                EdgeCenters,
                EdgeLinearEqs,
                Destination,
                NotARoute,
                BaseEdgeIdx))

            return AngleEdgeWeights
            # print('\n\nThe angle weights are:')
            # print(AngleEdgeWeights)
            # print('\n\n')

    def getAdyacentAngleWeight(self):
        RouteEdgetoAdyacentEdges = {}

        getRouteIntersectionOptions = \
            self.myEdgeDataExtractor.getEdgeToInsersectionDict()

        DecisionEdgeCenters = []
        DecisionEdgeLinEqs = []
        for EdgeinRoute in self.Route_Edges:
            if (getRouteIntersectionOptions[EdgeinRoute]):
                TempEdgeCenter = []
                TempEdgeLinEq = []
                for Edge in getRouteIntersectionOptions[EdgeinRoute]:
                    TempEdgeCenter.append(self.EdgetoEdgeCenter[Edge])
                    TempEdgeLinEq.append(self.EdgeLinearEquation[Edge])

                DecisionEdgeCenters.append(TempEdgeCenter)
                DecisionEdgeLinEqs.append(TempEdgeLinEq)

        # print(DecisionEdgeLinEqs)
        # print(DecisionEdgeCenters)
        for i, _ in enumerate(DecisionEdgeCenters):
            # print('\nprocessDecisionWeightsForEdges')
            # print('La cuenta va en', i)
            # print(DecisionEdgeCenters[i])

            if (i < (len(DecisionEdgeCenters) - 2)):
                # print(self.currentEdgeCenters[i+1])
                # last Edge is destination,
                # one before last edge has a edge as
                # one of the destionation
                # two edge sets have to be removed.
                temp = self.processDecisionWeightsForEdges(
                    DecisionEdgeCenters[i],
                    DecisionEdgeLinEqs[i],
                    self.currentEdgeCenters[-1],
                    True,
                    i)
                RouteEdgetoAdyacentEdges.setdefault(self.Route_Edges[i], [])
                RouteEdgetoAdyacentEdges[self.Route_Edges[i]].append(temp)
        print(RouteEdgetoAdyacentEdges)

    def setTestMode(self):
        # print('Test Mode Started')
        # print(self.currentEdgeCenters)
        self.processDecisionWeightsForEdges(
            self.currentEdgeCenters,
            self.currentEdgeLinearEquation,
            self.currentEdgeCenters[-1])

        self.getAdyacentAngleWeight()

    def __findVectorDirection(self,
                              EdgeCenters,
                              EdgeLinEqs,
                              NotARoute=False,
                              BaseEdgeIdx=0):
        myGeometryAPI = GeometryClass()
        eval_val = myGeometryAPI.getBoundary_Y()
        len_EC = len(EdgeCenters)
        VectorPointDirection = []
        for i, EdgeCenter in enumerate(EdgeCenters):
            # print(EdgeCenter)
            if(((len_EC - 1) > i) and (not NotARoute)):
                # Find the closest value to point to find vector direction
                # From the current value of X, two Y's will be calculated
                # by substracting and adding the largestvalue vertical value
                # of the map (chosen arbitrarily)
                x_rng = \
                        [(eval_val*(-1)) + float(EdgeCenter[0]),
                         eval_val + float(EdgeCenter[0])]

                y_neg = \
                    ((EdgeLinEqs[i][0])*x_rng[0]) + EdgeLinEqs[i][1]

                y_pos = \
                    ((EdgeLinEqs[i][0])*x_rng[1]) + EdgeLinEqs[i][1]

                # The distance between that far point will be calculated
                # for the next point on route, this will allow to
                # discriminate which distant point is the closest to
                # the destination point. This distant point will be returned
                # in order to build the Vector of the origin point
                # (The current EdgeCenter iteration variable))

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

                # A list will be created with all the DistantVectorPoints
                # that are related to the EdgeCenters input list

                VectorPointDirection.append(distantVectorPoint)
                # angleBetweenEdges = \
                #    myGeometryAPI.getAngleBetweenVectors(
                #        distantVectorPoint,
                #        [float(EdgeCenters[i+1][0]),
                #         float(EdgeCenters[i+1][1])],
                #        [float(EdgeCenter[0]),
                #         float(EdgeCenter[1])])
            elif (NotARoute):
                # Find the closest value to point to find vector direction
                # From the current value of X, two Y's will be calculated
                # by substracting and adding the largestvalue vertical value
                # of the map (chosen arbitrarily)
                x_rng = \
                    [(eval_val*(-1)) +
                     float(EdgeCenter[0]),
                     eval_val +
                     float(EdgeCenter[0])]

                y_neg = \
                    ((EdgeLinEqs[i][0])*x_rng[0]) +\
                    EdgeLinEqs[i][1]

                y_pos = \
                    ((EdgeLinEqs[i][0])*x_rng[1]) +\
                    EdgeLinEqs[i][1]

                # The distance between that far point will be calculated
                # for the next point on route, this will allow to
                # discriminate which distant point is the closest to
                # the destination point. This distant point will be returned
                # in order to build the Vector of the origin point
                # (The current EdgeCenter iteration variable))

                neg_dist = myGeometryAPI.getDistance(
                    [x_rng[0], y_neg],
                    [float(self.currentEdgeCenters[BaseEdgeIdx][0]),
                     float(self.currentEdgeCenters[BaseEdgeIdx][1])])

                pos_dist = myGeometryAPI.getDistance(
                    [x_rng[1], y_pos],
                    [float(self.currentEdgeCenters[BaseEdgeIdx][0]),
                     float(self.currentEdgeCenters[BaseEdgeIdx][1])])

                if(neg_dist > pos_dist):
                    distantVectorPoint = [x_rng[0], y_neg]
                else:
                    distantVectorPoint = [x_rng[1], y_pos]

                # A list will be created with all the DistantVectorPoints
                # that are related to the EdgeCenters input list

                VectorPointDirection.append(distantVectorPoint)

        return VectorPointDirection

    # def __setattr__(self, name, value):
        # print(bcolors.WARNING + 'ERROR: The attribute ' +
        #      name + ' doesnt exist' + bcolors.ENDC)

    # def __getattribute__(self, name):
        # print(bcolors.WARNING + 'ERROR: The attribute ' +
        #      name + ' doesnt exist' + bcolors.ENDC)


# myRoute = traci.route()

# myRouteAnalysis = RouteAnalysis(myRoute)
# print(myRouteAnalysis)
