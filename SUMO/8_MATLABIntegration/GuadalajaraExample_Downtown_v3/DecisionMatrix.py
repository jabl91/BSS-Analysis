## @package DecisionMatrix
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
# import os
import math
import random


## This class implements the core method to analyze all the edges on a
#  route and then assign the correspoding probabilities to each of them in
#  order to decide which one is likely that a agent will take based on the
#  agent based model of CopenhagenABM.
class DecisionMatrix:

    ## This is the constructor method
    def __init__(self):
        ## @var initFlag
        #  The purpose of this flag is to analyze that the constructor
        #  method has been called before using this any other class
        #  method.
        #  @remarks
        #  Not yet implemented.
        self.initFlag = True

    ## This method will take several decision vectors and then sum all of the
    #  elements on for each of the vectors. This is what is needed in order
    #  to calculate the probability of each of the vectors.
    #  @remarks
    #  The name of this method has been indentified to not represent what
    #  the method description specifies. This method name will be changed
    #  in future releases.
    #  @param DecisionVector
    #  It contains several vectors for which of its values corresponds to
    #  the weights of every descriptor for the agent based model of
    #  CopenhagenABM. All the vectors contained on DecisionVector will be
    #  used in the Multinomial Linear regression model in order to decide
    #  the edge that has a higher probability of being chosen.
    def MultinomialRegression(self, DecisionVector):
        VectorDimension = \
            len(DecisionVector[list(DecisionVector.keys())[0]][0])
        SumOfElements = [0 for x in range(VectorDimension)]
        for i, element in enumerate(DecisionVector.keys()):
            for j, value in enumerate(DecisionVector[element][0]):
                SumOfElements[j] = SumOfElements[j] + value

        return SumOfElements

    ## This method will calculate the probability of a set of all vector
    #  elements sum of the edges that want to be selected to follow within the
    #  next edge on route. It is important to mention that even though
    #  this method refers to probabilities, they will not yet be transformed
    #  into a 0-1 probability range. This will be done by another method, refer
    #  to #calculateFinalProbability.
    #  @param SumVector
    #  It is just a list of the sum of the elements of different decision
    #  vectors
    def calculateProbability(self, SumVector):
        Probabilities = []
        if(len(SumVector) > 1):
            for j in range(len(SumVector)):
                Prob_divisor = 0
                for i, element in enumerate(SumVector):
                    if(i != j):
                        Prob_divisor += math.exp(element)
                # The formula is just that the addition of all the elements
                # within SumVector, the result of that is used as the
                # exponent of $e$. then that value is divided by the sum
                # of every element of SumVector that previosly was evaluate as
                # $e^x$ where $x$ is the SumVector element. It is important to
                # mention that this will have to be done for each SumVector
                # element and the dividend will always discard the value of
                # $e^x$ when $x$ is the current SumVector element
                Probabilities.append(math.exp(sum(SumVector)) /
                                     Prob_divisor)
        else:
            # In case there is only one element, then no calculation needs
            # to be done because the probability of a single decision element
            # will always be one.
            Probabilities.append(1.0)

        return Probabilities

    ## This method will grab all the probabilities that were calculated by
    #  #calculateProbability and then convert them into a 0-1 probability
    #  range.
    #  @ProbVector
    #  This is a list of previously calculated probabilities based on a
    #  multinomial linear regression model.
    def calculateFinalProbability(self, ProbVector):
        FinalProb = []
        if(len(ProbVector) > 1):
            for j in range(len(ProbVector)):
                Prob_divisor = 0
                for i, element in enumerate(ProbVector):
                    Prob_divisor += element
                # This final probability is just the current probability
                # that is being analyzed from ProbVector divided by
                # the sum of all the elements contained in ProbVector.
                FinalProb.append(ProbVector[j] /
                                 Prob_divisor)
            # print(FinalProb)
        else:
            FinalProb.append(1.0)
        return FinalProb

    ## This method imlements a stochastic selection of the probabilities that
    #  were calculated by #calculateFinalProbability. The random
    #  algorithm is the one that python provides, a new entropy source can
    #  be consider to increase the randomness factor.
    #  @param ProbVector
    #  List of probabilities calculated by #calculateFinalProbability
    def StochasticSelection(self, ProbVector):
        MyVector = list(range(0, len(ProbVector)))
        myChoice = random.choices(MyVector, weights=ProbVector)
        # print(myChoice[0])
        return myChoice[0]

    ## This method is the main core of #DecisionMatrix, it will grab all the
    #  calculated weights that refer to each of the weights that are
    #  described by the agent based model of CopenhagenABM.
    #  @param RoadOptionsIdx
    #  This is a dictionary that maps the route edges into the possible
    #  edges that can be connected to. For example, a route edge will be
    #  connected into an intersection and the vehicle which is driving on
    #  the current route edge will have to take a decision to which
    #  edge it has to go now.
    #  @param AngleEdgeWeights
    #  This is a dictionary with the angle edge weights that belong to
    #  each route edge.
    #  @param AvoidUTurn
    #  This is a dictionary with the information about which edges
    #  will trigger a UTurn based on the current route edges.
    #  @param SecondaryRoad
    #  This dictionary will contain the information wether the edges are
    #  Secondary road or not. (Classification based on CopenhagenABM model)
    #  @param MultiStoreyHousing
    #  This dictionary will contain the information wether along the edges
    #  there are multi storey housing (buildings with houses).
    #  @param GreenPercent
    #  This dictionary will contain the information wether along the edges
    #  there are green areas (trees, grass, parks, etc). For example, is all
    #  the edge is a park edge, then this will be 100%. If only a portion of
    #  the edge has "green areas" then a percentage has to be calculated.
    #  @param CycleTrackLane
    #  This dictionary will contain the information wether the edge has a
    #  dedicated lane for cyclists.
    #  @param NotAlreadyVisited
    #  This dictionary will contain the information wether the edge has already
    #  been visited within the current trip of the vehicle.
    #  @param CyclePath
    #  This dictionary will contain the information wether the edge is a fully
    #  dedicated cycling path were there are no other type of vehicles going
    #  through.
    #  @param Path_Ped_Bikes
    #  This is a dictionary that will contain the information wether the edge
    #  is dedicated to cyclist and pedestrians.
    #  @param Residential_Street
    #  This is a dictionary that will contain the information wether the edge
    #  is a residential street or not.
    #  @param HousingWShops
    #  This is a dictionary that will contain the information wether the edge
    #  is a commercial area where there could be houses as well.
    #  @param TurnDirection
    #  This is a dictionary that will contain the information wether the edge
    #  that is being analyzed requires the vehicle to turn in any direction
    #  to continue its way.
    #  @param currentRouteEdges
    #  This is a list of the edges that the current route has.
    #  @param UnknownParameter
    #  This parameter is defined on CopenhagenABM, however no information
    #  on what it is needed for or what it represents was given by the
    #  CopenhagenABM documentation.
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

            # In the case of the TurnDirection input, this list has all
            # the possible alternatives for the vehicle to continue its
            # way. Therefore, for the agent based model it is needed to
            # create two different lists, one for right/left direction
            # and another one for UTURN only. Moreover, it is considered
            # that if a UTurn has to be done, the vehicle is always turning
            # left.
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

            # This array just simplifies the way each of the Input
            # packages are going to be accessed.
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

            # Every route edge will have to be evaluated, the following
            # for statement will just iterate over each of the edges and
            # only the iteration variable will be used.
            for interIdx, _ in enumerate(currentRouteEdges):
                # The following is needed because the last two
                # edges are not part of the angle calculation
                # due to restrictions on mathematical formula
                if(interIdx < len(currentRouteEdges) - 2):
                    BalancedWeights = {}
                    # This for statement will evaluate each of the elements
                    # that correspond to the current route edge with respect
                    # to the InputPackage.
                    for i, input in enumerate(InputPackage):
                        # If there is something on the one of the input
                        # packages then do the following code.
                        if(input):
                            # Values are retrieved for the correspoding
                            # route edge
                            Values = input[currentRouteEdges[interIdx]]
                            Values = Values[0]

                            # Each of the values of the input package
                            # correspond to a specific weight value that
                            # is defined by the CopenhagenABM model.
                            # Each of the values of the input package needs
                            # to be multiplied by the corresponding weight.
                            for counter, value in enumerate(Values):
                                Values[counter] = \
                                    value * \
                                    myConsts.PROCESS_WEIGHTS_ORDERED_CONST[i]

                            # For every input element on the input package
                            # there is a dictionary that will contain all the
                            # values that are being analyzed. In this case,
                            # BalancedWeights will contain each of the
                            # DecisionMatrix elements 'DM_' for every route
                            # edge.
                            BalancedWeights.setdefault('DM_' + str(i), [])
                            BalancedWeights['DM_' + str(i)].append(Values)

                    # Once all the corresponding input elements of the input
                    # packages have been analyzed for a specific route edge,
                    # then all of those weights of those input elements will
                    # be appended to a list called AllBalancedWeights.
                    AllBalancedWeights.append(BalancedWeights)

            # The following will evaluate each of the previously
            # calculated weights in order to get a list of edges that are
            # likely for the user to take based on the CopenhagenABM model.
            myChoices = []
            for i, element in enumerate(AllBalancedWeights):

                ElementsSum = self.MultinomialRegression(element)
                Probabilities = self.calculateProbability(ElementsSum)
                FinalProbSet = self.calculateFinalProbability(Probabilities)
                myChoice = self.StochasticSelection(FinalProbSet)
                myChoices.append(myChoice)

            return myChoices
