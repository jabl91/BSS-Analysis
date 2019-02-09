
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
import traci


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

    def getBoundary_Y(self):
        traciBoundary_Y = traci.gui.getBoundary()
        traciBoundary_Y = \
            abs(traciBoundary_Y[0][1]) + \
            abs(traciBoundary_Y[1][1])
        return traciBoundary_Y

    def getAngleBetweenVectors(self, Vector1, Vector2, ref=[0, 0]):
        # print('\ngetAngleBetweenVectors')
        # print(Vector1)
        # print(Vector2)
        # print(ref)

        Vector1 = [float(i) for i in Vector1]
        Vector2 = [float(i) for i in Vector2]
        ref = [float(i) for i in ref]
        Vector1 = [Vector1[0] - ref[0], Vector1[1] - ref[1]]
        Vector2 = [Vector2[0] - ref[0], Vector2[1] - ref[1]]

        # print(Vector1, Vector2)

        distVector1 = self.getDistance([0, 0], Vector1)
        distVector2 = self.getDistance([0, 0], Vector2)

        # print(distVector1, distVector2)
        dotProduct = \
            (Vector1[0]*Vector2[0]) + (Vector1[1]*Vector2[1])

        # print(dotProduct)

        cosTheta = (dotProduct)/(distVector1*distVector2)

        if(cosTheta > 1.0):
            cosTheta = 1.0
        if(cosTheta < -1.0):
            cosTheta = -1.0

        return math.degrees(math.acos(cosTheta))


# myGeometryAPI = GeometryClass()
# print(myGeometryAPI.getAngleBetweenVectors([-2, 2], [2, 2], [0, 0]))
# myDistance = myGeometryAPI.getDistance([-5, -5], [0, 0])
# print(myDistance)

# mySlope, myIntercept = myGeometryAPI.getSlopeandIntercept([5, 8], [6, -5])
# print(mySlope, myIntercept)
