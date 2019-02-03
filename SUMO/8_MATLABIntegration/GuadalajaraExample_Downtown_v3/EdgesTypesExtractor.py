from __future__ import absolute_import
from __future__ import print_function
import xml.etree.ElementTree as ET


class EdgeTypesExtractor:

    STR_CYCLEWAY = 'cycleway'
    STR_HIGHWAY = 'highway'
    STR_RAILWAY = 'railway'

    # cyclepath is defined by (Snizek et al 2013) as
    # "we have classified the cycling infrastructure in the following
    # manner: street with no cycling facilities; cycle path by the
    # side of the road (separated from motor traffic by a curb); cycle lane
    # on the road (separated from motor traffic by markings on the
    # road); off-road path exclusively for cyclists, and finally off-road
    # path shared by cyclists and pedestrians.

    CONVERSION_DICT = {
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

    def __init__(self, netFile):
        self.tree = ET.parse(netFile)

    def __getTree(self):
        return self.tree

    def __getRoot(self):
        return self.tree.getroot()

    def findAllAvailableTypes(self):
        cycleway_types = []
        highway_types = []
        railway_types = []

        for myType in self.__getRoot().iter('type'):
            currentID = myType.attrib.get('id')
            if self.STR_CYCLEWAY in currentID:
                cycleway_types.append(currentID)
            if self.STR_HIGHWAY in currentID:
                highway_types.append(currentID)
            if self.STR_RAILWAY in currentID:
                railway_types.append(currentID)

        self.cycleway_set = set(cycleway_types)
        self.highway_set = set(highway_types)
        self.railway_set = set(railway_types)

        for match in self.cycleway_set & self.highway_set:
            self.highway_set.remove(match)

        for match in self.cycleway_set & self.railway_set:
            self.railway_set.remove(match)

        for match in self.highway_set & self.railway_set:
            self.railway_set.remove(match)

        waysDict = {self.STR_CYCLEWAY: self.cycleway_set,
                    self.STR_HIGHWAY: self.highway_set,
                    self.STR_RAILWAY: self.railway_set}

        return waysDict

    def getEdgeTypeDict(self):
        # self.findAllAvailableTypes()
        EdgeToEdgeType = {}
        for myEdge in self.__getRoot().iter('edge'):
            if(myEdge.attrib.get('type')):
                currentTypeSet = myEdge.attrib.get('type')
                if(self.CONVERSION_DICT[currentTypeSet]):
                    EdgeToEdgeType[myEdge.attrib.get('id')] = \
                            self.CONVERSION_DICT[currentTypeSet]
                else:
                    EdgeToEdgeType[myEdge.attrib.get('id')] = None

        return EdgeToEdgeType


# treeNet = ET.parse('osm.net.xml')
myExtractor = EdgeTypesExtractor('osm.net.xml')

print(myExtractor.getEdgeTypeDict())
# print(myExtractor.findAllAvailableTypes())
