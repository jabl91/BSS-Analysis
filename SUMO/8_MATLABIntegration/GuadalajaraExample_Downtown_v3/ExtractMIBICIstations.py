from __future__ import absolute_import
from __future__ import print_function
import xml.etree.ElementTree as ET
import math

tree = ET.parse('osm_bbox.osm.xml')
root = tree.getroot()

treeNet = ET.parse('osm.net.xml')
rootNet = treeNet.getroot()


treePoly = ET.parse('osm.poly.xml')
rootPoly = treePoly.getroot()

bikeStations = []
bikeStations_XY = []
dict_BikeStations = {}
# print(root)

# for child in root:
#    print child.tag, child.attrib

with open("EstacionesMIBICI.txt", "r") as bikeStationsFile:
    line = bikeStationsFile.readline()
    while line:
        type, value = line.strip().split(':')
        bikeStations.append(str(value))
        line = bikeStationsFile.readline()

# print (bikeStations)

for poi in rootPoly.iter('poi'):
    for station in bikeStations:
        if poi.attrib.get('id') == station:
            bikeStations_XY.append([
                                poi.attrib.get('x'),
                                poi.attrib.get('y')])

dict_BikeStations = zip(bikeStations, bikeStations_XY)
print(dict_BikeStations)

bikeStationsEdges = []

for currentStation, [X2, Y2] in dict_BikeStations:
    _, _, minedgeDistanceX, minedgeDistanceY = \
            rootNet.find('location'). \
            get('convBoundary').split(",")
    minedgeDistance = pow(float(minedgeDistanceX), 2) \
        + pow(float(minedgeDistanceY), 2)
    minedgeDistance = math.sqrt(minedgeDistance)
    for edge in rootNet.iter('edge'):
        if(edge.attrib.get('shape') is not None):
            for shapes in edge.attrib.get('shape').split(" "):
                X1, Y1 = shapes.split(",")
                tempDistanceX = pow(abs(float(X2) - float(X1)), 2)
                tempDistanceY = pow(abs(float(Y2) - float(Y1)), 2)
                tempDistance = math.sqrt(tempDistanceX + tempDistanceY)
                if(tempDistance < minedgeDistance):
                    minedgeDistance = tempDistance
                    nearestEdge = edge.attrib.get('id')
    bikeStationsEdges.append([currentStation, nearestEdge, minedgeDistance])

print(bikeStationsEdges)

with open("test/test.xml", "w") as myFile:
    print(
            '<routes>\n'
            '   <vType id="bike" length="0.6" width="0.2" '
            'vClass="bicycle"/>', file=myFile)
    myFlowCounter = 0
    for stationID, nearestEdge, _ in bikeStationsEdges:
        print(
                '   <flow id="bike_' + str(myFlowCounter) + '"'
                ' type="bike" from=' +
                '"' + str(nearestEdge) + '" ' + 'to=' + '"'
                + str(bikeStationsEdges[0][1]) +
                '" ' + 'begin="0" end="3000" number="50" '
                'departPos="random_free"/>', file=myFile)
        myFlowCounter = myFlowCounter + 1
    print("</routes>", file=myFile)
