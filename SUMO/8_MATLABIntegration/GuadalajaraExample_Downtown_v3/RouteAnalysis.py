## @package RouteAnalysis
# This package contains the required methods to calculate which
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

from EdgesTypesExtractor import EdgeTypesExtractor
from Geometry import GeometryClass
from DecisionMatrix import DecisionMatrix

import traci

# import math


## This class was implemented to help color each of the lines
#  that are shown on the console output. At the moment this module was written
#  there was no need of implementing this on any other module, however
#  this class may be implemented on a dedicated package in order to be used
#  by others.
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


## This is the class that implements all the logic behind the Route
#  identification of an specific route as well as it has APIs that
#  which help on deciciding which edges along the route are likely
#  to be followed by a vehicle based on the CopenhagenABM agent based model.
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

    ## This is the constructor
    def __init__(self):
        ## @var myRoute
        #  This attribute has the route id of an specific vehicle, this
        #  along with SUMO Traci APIs will provide all the information
        #  needed to take a deicision on which route to take
        self.myRoute = 'myRoute'

        ## @var myDecision
        #  This attribute will have the final decision on which is the route
        #  that was selected by using the agent based model.
        self.myDecision = 'CurrentRoute'

        ## @var AllLanes
        #  This atribute contains all the lanes that exist within the
        #  SUMO network file.
        self.AllLanes = traci.lane.getIDList()

        ## @var AllEdges
        #  This attribute contains all the edges that exist within the
        #  SUMO network file.
        self.AllEdges = traci.edge.getIDList()

        ## @var LaneToEdge
        #  This attribute implements a dictionary which keys are all the lanes
        #  that exist within the SUMO network file and the values are the
        #  corresponding edges which those lanes are attached to.
        for myLane in self.AllLanes:
            self.LaneToEdge[myLane] = traci.lane.getEdgeID(myLane)

        ## @var myEdgeDataExtractor
        #  This is an object from #EdgeTypesExtractor class which
        #  uses the 'osm.net.xml' to get all information related to current
        #  simulation network
        self.myEdgeDataExtractor = EdgeTypesExtractor('main.net.xml')

        ## @var EdgetoEdgeType
        #  This attribute obtains a dictionary which maps the name of the
        #  edge to its corresponding agent model edge descriptor
        #  (cycleway, cyclepath, residential, path, etc.)
        self.EdgetoEdgeType = \
            self.myEdgeDataExtractor.getEdgeTypeDict()

        ## @var EdgetoEdgeCenter
        #  This attribute is a dictionary that contains for keys all the
        #  possible edge ids and the values correspond to the center position
        #  with respect to the global simulation coordinates
        #  @var EdgeLinearEquation
        #  This attribute is a dictionary that contains for keys all the
        #  possible edge ids ant eh values correspond to a tuple of two
        #  elements, a intercept and slope that represent the linear equation
        #  that describes such edges on the global simulator map.
        self.EdgetoEdgeCenter, self.EdgeLinearEquation = \
            self.myEdgeDataExtractor.getCenterofEdgeDict()

    ## This is the string value when the object is operated as string.
    #  (e.g. print function)
    def __str__(self):
        return (bcolors.OKBLUE +
                '\nRouteAnalysis Class -- Description\n'
                'This class contains the required methods to calculate which\n'
                'routes are better than others taking into consideration\n'
                'the weights table proposed on Mapping cyclists experiences\n'
                'and agent-based modelling of their wayfinding behaviour\n'
                '(Snizek, 2015)\n' +
                bcolors.ENDC)

    ## This method has to be used to define which is Route
    #  that the #RouteAnalysis object will use to perform the analysis based
    #  on the agent based model
    #  @param myLocalRoute
    #  This parameter has to be the id of the route that needs to be
    #  analyzed
    def setCurrentRoute(self, myLocalRoute):
        self.myRoute = myLocalRoute
        self.getAllRoadsinRoute()

    ## This method just retrives the current route id that the
    #  #RouteAnalysis object uses.
    def getCurrentRoute(self):
        return self.myRoute

    ## This method returns all the ordered edges that below to the
    #  #RouteAnalysis object current route
    def getAllEdges(self):
        return traci.route.getEdges(self.myRoute)

    ## This method converts a lane id into an edge id, the edge id corresponds
    #  the edge that the lane belongs to.
    #  @param myLocalLane
    #  This parameter is the lane id.
    def convertVehicleLane2VehicleEdge(self, myLocalLane):
        return self.LaneToEdge[myLocalLane]

    ## This method obtains all the edges that are in the current route and
    #  fills several dictionaries with the information of each of those
    #  edges like edge center, edge intercept and slope pair and edge types
    #  (residential, path, cycleway, etc)
    def getAllRoadsinRoute(self):

        ## @var currentTypes
        #  This attribute contains an ordered list of the edge types
        #  (residential, path, cycleway, etc.) of the current route edges.
        self.currentTypes = []

        ## @var currentEdgeCenters
        #  This attribute contains an ordered list of the edge centers
        #  of the current route edges
        self.currentEdgeCenters = []

        ## @var currentEdgeLinearEquation
        #  This attribute contains an ordered list of the edge Linear
        #  equations of the current route edges
        self.currentEdgeLinearEquation = []

        ## @var Route_Edges
        #  This attribute contains an ordered list of all the edges that
        #  exist within the current route
        self.Route_Edges = []

        if traci.route.getEdges(self.myRoute):
            self.Route_Edges = traci.route.getEdges(self.myRoute)
            for myEdge in self.Route_Edges:
                self.currentTypes.append(
                    self.EdgetoEdgeType[myEdge])
                self.currentEdgeCenters.append(
                    self.EdgetoEdgeCenter[myEdge])
                self.currentEdgeLinearEquation.append(
                    self.EdgeLinearEquation[myEdge])

    ## This method implements a way to calculate the angle between two
    #  vectors which are defined by their centers and their linear
    #  equations. There are two ways to use this method, one of them is when
    #  the parameter NotARoute is True which means that EdgeCenters and
    #  EdgeLinearEq are orderded consecutevily based on the current route
    #  edges, this simplifies the algorithm to search the direction of the
    #  movement of the vehicle. The other option is when NotARoute is False
    #  which means all the EdgeCenters and Edge LinearEq are just the
    #  the corrsponding information of a set of edges which direction has to
    #  be inferred based on a base edge center defined by the parameter
    #  BaseEdgeIdx.
    #  @param EdgeCenters
    #  This could be a list of all the EdgeCenters of the edges along a route
    #  or a set of edge centers in which one of them will be consider to be
    #  the base edge for all calculations among that set
    #  @param EdgeLinearEq
    #  This could be a list of all the EdgeLinearEqs of the edges along a route
    #  or a set of edge linear equations in which one of them will be consider
    #  to be the base edge for all calculations among that set
    #  @param Destination
    #  This are the coordinates of the destination point where the vehicle is
    #  travelling to. This point and the base edge center describes a vector
    #  which direction always points from the base edge to the destination.
    #  @param NotARoute
    #  This parameter defined wether EdgeCenters and EdgeLinearEq are a list
    #  of consecutive edges along a predifined route (NotARoute == False) or
    #  those two list correspond just to a set of edges attributes in which one
    #  of them will be considered to be the base edge (NotARoute == True)
    #  @param BaseEdgeIdx
    #  This parameter only matters when NotARoute == True, it indicates
    #  which is the edge id that will be consider as a base for all the
    #  calculations
    def getAngleEdgeWeight(self,
                           EdgeCenters,
                           EdgeLinearEq,
                           Destination,
                           NotARoute=False,
                           BaseEdgeIdx=0):
        # An object of the class Geometry which implements the logic
        # behind the calculation of the angle between two vectors.
        myGeometryAPI = GeometryClass()
        EdgeAngleWeights = []

        # The next method will calculate the VectorPointDirection
        # this is needed to now the directions of the current
        # edge. This is done by taking the base edge center and calculating
        # to distant points that are within the the base edge linear equation
        # then those two distant points are used to calculate their
        # corresponding distance to the edge for which we want to know its
        # direction. For more information refer to #__findVectorDirection.

        VectorPointDirection = self.__findVectorDirection(
            EdgeCenters, EdgeLinearEq, NotARoute, BaseEdgeIdx)

        # Once the direction point of the other edge has been calculated
        # we can then use the #getAngleBetweenVectors API from the
        # #Geometry class in order to get all the corresponding angles.
        for i, DirectionPoint in enumerate(VectorPointDirection):
            EdgeAngleWeights.append(myGeometryAPI.getAngleBetweenVectors(
                DirectionPoint,
                Destination,
                EdgeCenters[i]))

        # The angle weight on the CopenhagenABM agent based model is
        # defined as the following formula $(1 - i/180.0)$ where $i$
        # corresponds to the angle between two vectors in degrees.
        EdgeAngleWeights = [(1 - i / 180.0) for i in EdgeAngleWeights]

        return EdgeAngleWeights

    ## This method is just a placeholder for #getAngleEdgeWeight
    #  there is no extra processing done in this function.
    #  It was implementd as a possible intermedite layer between
    #  function caller and #getAngleEdgeWeight
    #  @param EdgeCenters
    #  This could be a list of all the EdgeCenters of the edges along a route
    #  or a set of edge centers in which one of them will be consider to be
    #  the base edge for all calculations among that set
    #  @param EdgeLinearEq
    #  This could be a list of all the EdgeLinearEqs of the edges along a route
    #  or a set of edge linear equations in which one of them will be consider
    #  to be the base edge for all calculations among that set
    #  @param Destination
    #  This are the coordinates of the destination point where the vehicle is
    #  travelling to. This point and the base edge center describes a vector
    #  which direction always points from the base edge to the destination.
    #  @param NotARoute
    #  This parameter defined wether EdgeCenters and EdgeLinearEq are a list
    #  of consecutive edges along a predifined route (NotARoute == False) or
    #  those two list correspond just to a set of edges attributes in which one
    #  of them will be considered to be the base edge (NotARoute == True)
    #  @param BaseEdgeIdx
    #  This parameter only matters when NotARoute == True, it indicates
    #  which is the edge id that will be consider as a base for all the
    #  calculations
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

    ## This method retrieves three different dictionaries, one of them is
    #  a dictionary that contains as a key every of the edges that correspond
    #  to the current route. Each of the values will be the corresponding
    #  angle weights of the destination edges of every edge key. In other words
    #  for every edge on a route, there will be an intersection that refers to
    #  it, this intersection will have other edges to which the key edge can
    #  connect to so the vehicle can continue its way, in case any of those
    #  other edges are selected, a vector angle will be calculated between
    #  that edge and the destination edge. Refer to #getAngleEdgeWeight.
    #  For the second dictionary, its keys are the same as the previous one
    #  but the values are the other intersection edges turn direction. In other
    #  words, in case the key edge needs to connect to other edge in the
    #  intersection, the vehicle may have to turn left, right or even a uturn
    #  or continue straight.
    #  For the third dictionary, the key values are the same as the two
    #  previous ones and its values are just the corresponding intersection
    #  edges to which the key can connect to in order to allow the vehicle
    #  to continue its way.
    def getAdyacentAngleWeight(self):
        # This dictionary returns the angle weights of each of the edges
        # that can be part of the decision matrix when a route is selected
        # An angle weight is the angle between two vector that are formed
        # between the current analyzed edge and the vector from that edge
        # center to the final destination of the route
        RouteEdgetoAdyacentEdges = {}

        # This dictionary returns a list of the turn direction
        # of a edge in case a certain local destination edge is chosen
        # A local destination edge means such edges that are outlets of the
        # intersection where the input edge is being analyzed
        RouteEdgeToAdjEdgeTypes = {}

        # This dictionary returns a list of all the names of the edges that
        # are being analyzed within this function. The number of elements
        # in each list is the same as in the other dictionaries.
        RouteEdgeToDecisionEdges = {}

        # This method returns all the "outlets" that are associated to an edge
        # that enters an intersection. Refer to #getEdgeToInsersectionDict
        getRouteIntersectionOptions = \
            self.myEdgeDataExtractor.getEdgeToInsersectionDict()

        #  This method calculates the direction of the vehicle's movement
        #  when a edge has been taken after entering an intersection.
        #  Refer to #getEdgeToIntersection_DestType
        getRouteIntersectionDstTypes = \
            self.myEdgeDataExtractor.getEdgeToIntersection_DestType()

        DecisionEdgeCenters = []
        DecisionEdgeLinEqs = []
        for EdgeinRoute in self.Route_Edges:
            # If the edge exist on dictionary then procceed.
            if (getRouteIntersectionOptions[EdgeinRoute]):
                TempEdgeCenter = []
                TempEdgeLinEq = []
                TempEdgeDecision = []

                # For every other edge to which the key edge can connect
                # to within the intersection. The center of the edge,
                # the linear equation that describes that edge and the edge
                # id will be stored in three different temp lists.
                for Edge in getRouteIntersectionOptions[EdgeinRoute]:
                    TempEdgeCenter.append(self.EdgetoEdgeCenter[Edge])
                    TempEdgeLinEq.append(self.EdgeLinearEquation[Edge])
                    TempEdgeDecision.append(Edge)

                # Each temporary list will then mapped to a general list that
                # will contain lists of every set of edges that belong to each
                # intersection where the key edge can connect to.
                DecisionEdgeCenters.append(TempEdgeCenter)
                DecisionEdgeLinEqs.append(TempEdgeLinEq)

                # This dictionary returns a list of the turn direction
                # of a edge in case a certain local destination edge is chosen
                # A local destination edge means such edges that are outlets of
                # the intersection where the input edge is being analyzed
                RouteEdgeToAdjEdgeTypes.setdefault(EdgeinRoute, [])
                RouteEdgeToAdjEdgeTypes[EdgeinRoute].append(
                    getRouteIntersectionDstTypes[EdgeinRoute])

                # This dictionary returns a list of all the names of the edges
                # that are part of the intersection outlets. The number of
                # elements in each list is the same as in the other
                # dictionaries.
                RouteEdgeToDecisionEdges.setdefault(EdgeinRoute, [])
                RouteEdgeToDecisionEdges[EdgeinRoute].append(
                    TempEdgeDecision)

        for i, _ in enumerate(DecisionEdgeCenters):
            if (i < (len(DecisionEdgeCenters) - 2)):

                # The last edge of currentEdgeCenters is the destination edge.
                # One edge before the destination edge has a decision edge
                # which is the destination edge, so no analysis has to be
                # performed on this edge because the destiantion edge will
                # be always selected to be connected to this edge.
                # If N is the number of edges on currentEdgeCenters then,
                # only 0 to N-2 edges are needed because of what was described
                # here. For more information refer to #__findVectorDirection.
                temp = self.processDecisionWeightsForEdges(
                    DecisionEdgeCenters[i],
                    DecisionEdgeLinEqs[i],
                    self.currentEdgeCenters[-1],
                    True,
                    i)

                # This dictionary returns the angle weights of each of the
                # edges that can be part of the decision matrix when a route
                # is selected
                RouteEdgetoAdyacentEdges.setdefault(self.Route_Edges[i], [])
                RouteEdgetoAdyacentEdges[self.Route_Edges[i]].append(temp)

        return RouteEdgeToDecisionEdges,\
            RouteEdgetoAdyacentEdges,\
            RouteEdgeToAdjEdgeTypes

    ## This principal method that has to be called after the object
    #  has been created by the constructor method. This function will grab
    #  the current Route edges and then process to decided based on
    #  the methods on #DecisionMatrix which edges along the route are meant to
    #  be selected based on the agent based model of CopenhagenABM.
    def RA_mainFunction(self):

        # This method is here just to test purposes, it will be removed
        # from here on future releases.
        self.processDecisionWeightsForEdges(
            self.currentEdgeCenters,
            self.currentEdgeLinearEquation,
            self.currentEdgeCenters[-1])

        # This method will retrieve three dictionaries, one that contains
        # edge outlets for every edge key. The other the angle weights of
        # every edge outlet for every edge key and the last one contains
        # the turn direction of every edge outlet for every edge key. For more
        # information please refer to #getAdyacentAngleWeight.
        EdgesIdx, EdgesAngle, EdgesTurnDirection = \
            self.getAdyacentAngleWeight()

        # This is the core method for analyzing the route edges and
        # decide wether the user will take or not that route. For
        # more information refer to #DecisionMatrix
        myDecisionMatrix = DecisionMatrix()
        EdgeChoices = myDecisionMatrix.ProcessWeights(
            EdgesIdx,                               # EdgeIdx
            EdgesAngle,                             # ANGL_DEST
            False,                                  # avoid_u_turn
            False,                                  # E_TVEJ
            False,                                  # E_AND
            False,                                  # GROENPCT
            False,                                  # CTRACKLANE
            False,                                  # avoid_already_visited
            False,                                  # CSTI
            False,                                  # CFSTI
            False,                                  # E_LVEJ
            False,                                  # E_BUT
            EdgesTurnDirection,                     # Turn Direction
            self.getAllEdges())                     # Current Route Edges

        print('We can consider that every time this runs it will give an X \
              route that can be compared against the one that was given \
              by SUMO. If we do this X amount of times we can graph \
              wether the route has high probability of being choosen')

        print('The predifined route is')
        print(self.getAllEdges())
        print('The stochastic selection of routes is')
        for i, edge in enumerate(self.getAllEdges()):
            if i < len(EdgeChoices):
                print(EdgesIdx[edge][0][EdgeChoices[i]])

    ## This method will implement the logic behind the identification of
    #  an edge direction vector. In other words this means to identify the
    #  direction to which the edge is pointing to in the global simulation
    #  map.
    #  @param EdgeCenters
    #  This could be a list of all the EdgeCenters of the edges along a route
    #  or a set of edge centers in which one of them will be consider to be
    #  the base edge for all calculations among that set
    #  @param EdgeLinearEq
    #  This could be a list of all the EdgeLinearEqs of the edges along a route
    #  or a set of edge linear equations in which one of them will be consider
    #  to be the base edge for all calculations among that set
    #  @param NotARoute
    #  This parameter defined wether EdgeCenters and EdgeLinearEq are a list
    #  of consecutive edges along a predifined route (NotARoute == False) or
    #  those two list correspond just to a set of edges attributes in which one
    #  of them will be considered to be the base edge (NotARoute == True)
    #  @param BaseEdgeIdx
    #  This parameter only matters when NotARoute == True, it indicates
    #  which is the edge id that will be consider as a base for all the
    #  calculations
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

            # In case NotARoute == False, then we need to discard the last
            # two elements on EdgeCenters and EdgeLinEqs because the last
            # edge will be always the destination edge and one before that
            # one will always connect to the destination edge so no
            # decision calculation needs to be done.
            if(((len_EC - 1) > i) and (not NotARoute)):

                # Find the closest value to point to find vector direction
                # From the current value of X, two Y's will be calculated
                # by substracting and adding the largestvalue vertical value
                # of the map (chosen arbitrarily)
                x_rng = \
                    [(eval_val * (-1)) + float(EdgeCenter[0]),
                     eval_val + float(EdgeCenter[0])]

                y_neg = \
                    ((EdgeLinEqs[i][0]) * x_rng[0]) + EdgeLinEqs[i][1]

                y_pos = \
                    ((EdgeLinEqs[i][0]) * x_rng[1]) + EdgeLinEqs[i][1]

                # The distance between that far point will be calculated
                # for the next point on route, this will allow to
                # discriminate which distant point is the closest to
                # the destination point. This distant point will be returned
                # in order to build the Vector of the origin point
                # (The current EdgeCenter iteration variable))

                neg_dist = myGeometryAPI.getDistance(
                    [x_rng[0], y_neg],
                    [float(EdgeCenters[i + 1][0]),
                     float(EdgeCenters[i + 1][1])])

                pos_dist = myGeometryAPI.getDistance(
                    [x_rng[1], y_pos],
                    [float(EdgeCenters[i + 1][0]),
                     float(EdgeCenters[i + 1][1])])

                if(neg_dist < pos_dist):
                    distantVectorPoint = [x_rng[0], y_neg]
                else:
                    distantVectorPoint = [x_rng[1], y_pos]

                # A list will be created with all the DistantVectorPoints
                # that are related to the EdgeCenters input list
                VectorPointDirection.append(distantVectorPoint)

            # If what's being analyzed is not a route list of edges but a
            # set of edges that are being analyzed against one of them,
            # then the following code will be executed.
            elif (NotARoute):
                # Find the closest value to point to find vector direction
                # From the current value of X, two Y's will be calculated
                # by substracting and adding the largestvalue vertical value
                # of the map (chosen arbitrarily)
                x_rng = \
                    [(eval_val * (-1)) +
                     float(EdgeCenter[0]),
                     eval_val +
                     float(EdgeCenter[0])]

                y_neg = \
                    ((EdgeLinEqs[i][0]) * x_rng[0]) +\
                    EdgeLinEqs[i][1]

                y_pos = \
                    ((EdgeLinEqs[i][0]) * x_rng[1]) +\
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
