
# This file contains the required methods to decide which edge a
# cyclist is likely to take if a set of edges is given and also
# a final destination
# The analysis is also based in that project Git Repo that is located at
# https://github.com/bsnizek/CopenhagenABM

# @file    DecisionMatrix.py
# @author  Alberto Briseno
# @date    2019-02-09
# @version $Id$

from __future__ import absolute_import
from __future__ import print_function

from myPythonDependencies.myConstants import myConsts
import os
import math
import random


class DecisionMatrix:

    def __init__(self):
        self.initFlag = True
        # print('This is the Decision Matrix Class')

    def MultinomialRegression(self, DecisionVector):
        VectorDimension = \
            len(DecisionVector[list(DecisionVector.keys())[0]][0])
        SumOfElements = [0 for x in range(VectorDimension)]
        for i, element in enumerate(DecisionVector.keys()):
            for j, value in enumerate(DecisionVector[element][0]):
                SumOfElements[j] = SumOfElements[j] + value

        # print('The sum of elements is')
        # print(SumOfElements)

        return SumOfElements

    def calculateProbability(self, SumVector):
        Probabilities = []
        if(len(SumVector) > 1):
            for j in range(len(SumVector)):
                Prob_divisor = 0
                for i, element in enumerate(SumVector):
                    if(i != j):
                        Prob_divisor += math.exp(element)
                Probabilities.append(math.exp(sum(SumVector)) /
                                     Prob_divisor)
        else:
            Probabilities.append(1.0)
        # print(Probabilities)
        return Probabilities

    def calculateFinalProbability(self, ProbVector):
        FinalProb = []
        if(len(ProbVector) > 1):
            for j in range(len(ProbVector)):
                Prob_divisor = 0
                for i, element in enumerate(ProbVector):
                    Prob_divisor += element
                FinalProb.append(ProbVector[j] /
                                 Prob_divisor)
            # print(FinalProb)
        else:
            FinalProb.append(1.0)
        return FinalProb

    def StochasticSelection(self, ProbVector):
        MyVector = list(range(0, len(ProbVector)))
        myChoice = random.choices(MyVector, weights=ProbVector)
        # print(myChoice[0])
        return myChoice[0]


    def ProcessWeights(
            self,
            RoadOptionsIdx,         # List of Idx
            AngleEdgeWeights,       # Range 0 - 1       ANGL DEST
            AvoidUTurn,             # Boolean 0 or 1    avoid_u_turn
            SecondaryRoad,          # Boolean 0 or 1    E_TVEJ
            MultiStoreyHousing,     # Boolean 0 or 1    E_AND
            GreenPercent,           # Range 0 - 1       GROENPCT
            CycleTrackLane,         # Boolean 0 or 1    CTRACKLANE
            NotAlreadyVisited,      # Boolean 0 or 1    avoid_already_visited
            CyclePath,              # Boolean 0 or 1    CSTI
            Path_Ped_Bikes,         # Boolean 0 or 1    CFSTI
            Residential_Street,     # Boolean 0 or 1    E_LVEJ
            HousingWShops,          # Boolean 0 or 1    E_BUT
            TurnDirection,          # String List       *Instead of next two
            # LeftTurn,             # Boolean 0 or 1    left
            # RightTurn,            # Boolean 0 or 1    right
            currentRouteEdges,      # List Route Edges
            UnknownParameter=0):    # Boolean 0 or 1    E_HOJ

            UTurnDict = {}
            for i, key in enumerate(TurnDirection.keys()):
                tempList = []
                tempList2 = []
                for j, value in enumerate(TurnDirection[key][0]):
                    if(value == 'RTurn'):
                        tempList.append(myConsts.RIGHT)
                        tempList2.append(myConsts.AVOID_U_TURN)
                    elif(value == 'LTurn'):
                        tempList.append(myConsts.LEFT)
                        tempList2.append(myConsts.AVOID_U_TURN)
                    elif(value == 'UTurn'):
                        tempList.append(myConsts.LEFT)
                        tempList2.append(0.0)
                    else:
                        tempList.append(0.0)
                        tempList2.append(myConsts.AVOID_U_TURN)
                TurnDirection[key][0] = tempList
                UTurnDict[key] = [tempList2]
                AvoidUTurn = UTurnDict

            InputPackage = [
                # RoadOptionsIdx,
                AngleEdgeWeights,
                AvoidUTurn,
                SecondaryRoad,
                MultiStoreyHousing,
                GreenPercent,
                CycleTrackLane,
                NotAlreadyVisited,
                CyclePath,
                Path_Ped_Bikes,
                Residential_Street,
                HousingWShops,
                TurnDirection]

            AllBalancedWeights = []
            for interIdx, _ in enumerate(currentRouteEdges):
                # The following is needed because the last two
                # edges are not part of the angle calculation
                # due to restrictions on mathematical formula
                if(interIdx < len(currentRouteEdges) - 2):
                    BalancedWeights = {}
                    for i, input in enumerate(InputPackage):
                        if(input):
                            # print('input, interIdx, currentRE, i')
                            # print(input)
                            # print(interIdx)
                            # print(currentRouteEdges[interIdx])
                            # print(i)
                            Values = input[currentRouteEdges[interIdx]]
                            Values = Values[0]
                            for counter, value in enumerate(Values):
                                # print(value)
                                # print(myConsts.PROCESS_WEIGHTS_ORDERED_CONST[i])
                                Values[counter] = \
                                    value * \
                                    myConsts.PROCESS_WEIGHTS_ORDERED_CONST[i]
                            # print(Values)
                            BalancedWeights.setdefault('DM_'+str(i), [])
                            BalancedWeights['DM_'+str(i)].append(Values)
                    AllBalancedWeights.append(BalancedWeights)
            # print(AllBalancedWeights)
            # print('Done')

            myChoices = []
            for i, element in enumerate(AllBalancedWeights):

                # print('CurrentElement is ' + str(i))
                # print(element)
                ElementsSum = self.MultinomialRegression(element)
                Probabilities = self.calculateProbability(ElementsSum)
                FinalProbSet = self.calculateFinalProbability(Probabilities)
                myChoice = self.StochasticSelection(FinalProbSet)
                myChoices.append(myChoice)

            # print(myChoices)
            return myChoices
