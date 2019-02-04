
# This file contains the required methods to calculate which
# routes are better than others taking into consideration
# the weights table proposed on Mapping cyclists' experiences
# and agent-based modelling of their wayfinding behaviour(Snizek, 2015)
# The analysis is also based in that project Git Repo that is located at
# https://github.com/bsnizek/CopenhagenABM

# @file    Geometry.py
# @author  Alberto Briseno
# @date    2019-02-04
# @version $Id$

import math


class GeometryClass:

    def getSlopeandIntercept(self, Point1, Point2, zeroDivision=None):
        slope = None
        intercept = None

        if(Point1[0] != Point2[0]):
            slope = (Point1[1] - Point2[1]) / \
                     (Point1[0] - Point2[0])
        else:
            if(zeroDivision):
                slope = zeroDivision
            else:
                slope = float('Inf')

        intercept = (Point1[1]) - (slope * Point1[0])

        return slope, intercept

    def getDistance(self, Point1, Point2):
        distance = None
        distance = math.sqrt(
            pow((Point1[1] - Point2[1]), 2) +
            pow((Point1[0] - Point2[0]), 2))
        return distance


# myGeometryAPI = GeometryClass()
# myDistance = myGeometryAPI.getDistance([-5, -5], [0, 0])
# print(myDistance)

# mySlope, myIntercept = myGeometryAPI.getSlopeandIntercept([5, 8], [6, -5])
# print(mySlope, myIntercept)
