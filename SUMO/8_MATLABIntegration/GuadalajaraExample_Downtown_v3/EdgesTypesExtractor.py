
## @package EdgesTypesExtractor
#  This module implements the extraction of features of the network netFile
#  which is given by the SUMO netRouter. This extraction is done before
#  the execution of the simulation, this reduces heavily the runtime
#  processing that is needed.


from __future__ import absolute_import
from __future__ import print_function
import xml.etree.ElementTree as ET

# import traci
from myPythonDependencies.myConstants import myConsts
from Geometry import GeometryClass


## This the main class that implements all the methods to extract
#  the information from the netFile.
#  @remark Cyclepath is defined by (Snizek et al 2013) as
#  "we have classified the cycling infrastructure in the following
#  manner: street with no cycling facilities; cycle path by the
#  side of the road (separated from motor traffic by a curb); cycle lane
#  on the road (separated from motor traffic by markings on the
#  road); off-road path exclusively for cyclists, and finally off-road
#  path shared by cyclists and pedestrians.


class EdgeTypesExtractor:

    STR_CYCLEWAY = 'cycleway'
    STR_HIGHWAY = 'highway'
    STR_RAILWAY = 'railway'

    ## This is a dictionary that converts all the OpenStreetMaps (R)
    #  edge descriptors into a minimal subset of owned defined descriptors
    #  this will simplify the analysis and it will make them match them
    #  descriptors that are expected by the CopenhagenABM agent model.
    DECISION_CONVER_DICT = {
        'cycleway.lane': 'cyclepath',
        'cycleway.opposite_lane': 'cyclepath',
        'cycleway.opposite_track': 'cyclepath',
        'cycleway.track': 'cyclepath',
        'highway.bridleway': 'residential',
        'highway.bus_guideway': 'residential',
        'highway.cycleway': 'cyclepath',
        'highway.footway': 'residential',
        'highway.ford': 'residential',
        'highway.living_street': 'residential',
        'highway.motorway': 'residential',
        'highway.motorway_link': 'residential',
        'highway.path': 'path',
        'highway.pedestrian': 'residential',
        'highway.primary': 'housingWshops',
        'highway.primary_link': 'housingWshops',
        'highway.raceway': 'residential',
        'highway.residential': 'residential',
        'highway.secondary': 'secondary',
        'highway.secondary_link': 'secondary',
        'highway.service': 'secondary',
        'highway.stairs': 'residential',
        'highway.step': 'residential',
        'highway.steps': 'residential',
        'highway.tertiary': 'secondary',
        'highway.tertiary_link': 'secondary',
        'highway.track': 'residential',
        'highway.trunk': 'residential',
        'highway.trunk_link': 'residential',
        'highway.unclassified': 'residential',
        'highway.unsurfaced': 'residential',
        'railway.light_rail': 'railway',
        'railway.preserved': 'railway',
        'railway.rail': 'railway',
        'railway.subway': 'railway',
        'railway.tram': 'railway'}

    cycleway_set = []
    highway_set = []
    railway_set = []

    ## The constructor.
    #  @param netFile represents the xml file that contains all the network
    #         information that is provided by SUMO. The default name of
    #         this file is 'osm.net.xml'
    def __init__(self, netFile):
        ## @var tree
        #  XML Tree pointer
        self.tree = ET.parse(netFile)

    ##  This internal method returns the tree pointer of the xml file
    #   @param self The object pointer.
    def __getTree(self):
        return self.tree

    ##  This internal method returns the tree root pointer of the xml file
    #   @param self The object pointer.
    def __getRoot(self):
        return self.tree.getroot()

    ## This method extracts all the possible edges descriptors
    #  on regards to a classification of 3 elements (highway, railway or
    #  cicleway). Once it extracts all the combinations that exist
    #  on the netFile it will remove all the duplicated elements
    #  and it will provide a dictionary of all the sets of options
    #  that are associated to the 3 elements mentioned before.
    #  @param self The object pointer.
    #  @return A dictionary that contains all the possible edge
    #          descriptors regarding three different classification classes,
    #          highway, railway or cicleway.
    def findAllAvailableTypes(self):

        # Temporary lists that will be used to categorize the
        # sets of edge descriptors.
        cycleway_types = []
        highway_types = []
        railway_types = []

        # All different types of edge descriptors will be unclassified
        # among three different elements (cycleway, highway and railway)
        for myType in self.__getRoot().iter('type'):
            currentID = myType.attrib.get('id')
            if self.STR_CYCLEWAY in currentID:
                cycleway_types.append(currentID)
            if self.STR_HIGHWAY in currentID:
                highway_types.append(currentID)
            if self.STR_RAILWAY in currentID:
                railway_types.append(currentID)

        # All different types of edges descriptors will be converted into
        # sets in order to be able to apply operations like union, intersection
        # and difference.
        ## @var cycleway_set
        #  Set of all the edge types that are related to a cycleway.
        self.cycleway_set = set(cycleway_types)
        ## @var highway_set
        #  Set of all the edge types that are related to a highway.
        self.highway_set = set(highway_types)
        ## @var railway_set
        #  Set of all the edge types that are related to a railway.
        self.railway_set = set(railway_types)

        # All the same set elements between cycleway set and highway set
        # will be identified and the duplicates will be deleted from highway
        # set. This is done on purpose so every time a there is a highway
        # edge that contains a dedicated lane for cycleways, then it would
        # be easier from the implementation perspective to just consider it
        # as a cycleway and assign its associated weight into the
        # multinomial linear regression model
        for match in self.cycleway_set & self.highway_set:
            self.highway_set.remove(match)

        for match in self.cycleway_set & self.railway_set:
            self.railway_set.remove(match)

        for match in self.highway_set & self.railway_set:
            self.railway_set.remove(match)

        # A dictionary is returned by the function which contains all the
        # possible sets of values that can be found within the netFile
        # grouped by the 3 descriptors that are expected by the agent model.
        waysDict = {self.STR_CYCLEWAY: self.cycleway_set,
                    self.STR_HIGHWAY: self.highway_set,
                    self.STR_RAILWAY: self.railway_set}

        return waysDict

    ## This method is an improved analysis to retrieve the edge
    #  descriptor of every of the possible edges that are contained within
    #  the netFile. Instead of creating a dictionary during runtime,
    #  an already defined table #DECISION_CONVER_DICT is used to create
    #  a dictionary that maps the name of the edge to its corresponding
    #  agent model edge descriptor (cycleway, cyclepath, residential,
    #  path, etc.)
    def getEdgeTypeDict(self):
        # self.findAllAvailableTypes()
        EdgeToEdgeType = {}
        for myEdge in self.__getRoot().iter('edge'):
            if(myEdge.attrib.get('type')):
                currentTypeSet = myEdge.attrib.get('type')
                if(self.DECISION_CONVER_DICT[currentTypeSet]):
                    EdgeToEdgeType[myEdge.attrib.get('id')] = \
                        self.DECISION_CONVER_DICT[currentTypeSet]
                else:
                    EdgeToEdgeType[myEdge.attrib.get('id')] = None

        return EdgeToEdgeType

    ## This method iterates over all the edges that are defined on the
    #  netFile and returns two dictionaries, one that contains all the edge
    #  centers and the other one which contains the corresponding slope
    #  and intercept of every of those edges.
    # @return One dictionary that has all the netFile edge names as
    #          keys and the values are the center of those edges.
    # @return  Another dictonary that has all the netFile edge names
    #          as keys and the values as the slope and intercept that
    #          describes those edges based on the global map coordinates
    #  @sa #GeometryClass
    def getCenterofEdgeDict(self):
        # Geometry Class implements several trgonometrics APIs
        # that will be ued within this function to find the edge
        # centers as well as the linear equation that describes each of them
        myGeometryAPI = GeometryClass()

        # These two dictionaries are initialized and each of them will
        # represent the output of the function
        EdgetoEdgeCenter = {}
        EdgeLinearEquation = {}

        # The netFile will be analyzed and all defined edges will be iterated.
        # It is assumed that a single lane will be sufficient to calculate
        # the center of the edge. However, this assumption creates a small
        # center offset that will be inherent to the final value.
        # A better implementation would be to take the center of all the lanes
        # that are attached to an edge and then average them to get the
        # true edge center.
        # Based on the actual difference, the former algorithm works fine
        # for the agent model

        for myEdge in self.__getRoot().iter('edge'):
            if(myEdge.findall('lane')):
                myLanes = myEdge.findall('lane')
                myShape = myLanes[0].attrib.get('shape')
                myPoints = myShape.split()
                myPoints = [i.split(',') for i in myPoints]
                myPoints = myPoints[0] + myPoints[1]
                myPoints = list(map(float, myPoints))
                PosX = ((myPoints[0] + myPoints[2]) / 2.0)
                PosY = ((myPoints[1] + myPoints[3]) / 2.0)

                traciBoundary_Y = myGeometryAPI.getBoundary_Y()

                m_Edge, b_Edge = GeometryClass.getSlopeandIntercept(
                    myPoints[0:2], myPoints[2:4], traciBoundary_Y)

                EdgetoEdgeCenter[myEdge.attrib.get('id')] = \
                    ['{:.3f}'.format(item) for item in [PosX, PosY]]

                EdgeLinearEquation[myEdge.attrib.get('id')] = \
                    [m_Edge, b_Edge]

        return EdgetoEdgeCenter, EdgeLinearEquation

    ## This method returns all the "outlets" that are associated to an edge
    #  that enters an intersection. In other words, if a vehicle arrives to a
    #  intersection, it would have to choose between all the possible edges in
    #  which it can continue its movement
    #  @return A dictionary which keys maps to every edge on the Netfile and
    #          their values are all the options that a car has once it arrives
    #          into an intersection
    def getEdgeToInsersectionDict(self):
        EdgeToEdgeConnection = {}
        for myRoadConnection in self.__getRoot().iter('connection'):
            currentRoad = myRoadConnection.attrib.get('from')
            destinationRoad = myRoadConnection.attrib.get('to')
            EdgeToEdgeConnection.setdefault(currentRoad, [])
            EdgeToEdgeConnection[currentRoad].append(destinationRoad)
            # if(currentRoad in EdgeToEdgeConnection.keys()):
            #    EdgeToEdgeConnection[currentRoad] = \
            #        [EdgeToEdgeConnection[currentRoad], destinationRoad]
        # print(EdgeToEdgeConnection)
        return EdgeToEdgeConnection


    ## This method calculates the direction of the vehicle's movement
    #  when a edge has been taken after entering an intersection
    #  this information is highly relevant for the agent model decision
    #  matrix.
    #  @return A dictionary which keys are all the edges that are defined
    #          within the netFile. Their values are the "outlet" edges
    #          that are associated to the corresponding "inlet" edge
    #          intersection.
    #  @remark The return value of this method should be ordered with
    #          the one provided by #getEdgeToInsersectionDict, so a correct
    #          mapping can be inferred.
    def getEdgeToIntersection_DestType(self):

        EdgeToEdgeDstType = {}
        for myRoadConnection in self.__getRoot().iter('connection'):
            currentRoad = myRoadConnection.attrib.get('from')
            DstType = myRoadConnection.attrib.get('dir')
            EdgeToEdgeDstType.setdefault(currentRoad, [])
            EdgeToEdgeDstType[currentRoad].append(myConsts.DEST_TYPES[DstType])
            # if(currentRoad in EdgeToEdgeConnection.keys()):
            #    EdgeToEdgeConnection[currentRoad] = \
            #        [EdgeToEdgeConnection[currentRoad], destinationRoad]
        # print(EdgeToEdgeConnection)
        return EdgeToEdgeDstType


# treeNet = ET.parse('osm.net.xml')
# myExtractor = EdgeTypesExtractor('osm.net.xml')
# myExtractor.getEdgeToInsersectionDict()

# print(myExtractor.getCenterofEdgeDict())
# print(myExtractor.getEdgeTypeDict())
# print(myExtractor.findAllAvailableTypes())
