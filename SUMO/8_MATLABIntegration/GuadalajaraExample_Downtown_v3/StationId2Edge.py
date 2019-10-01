
import xml.etree.ElementTree as ET
# import sys
# import math
from Geometry import GeometryClass


def relativeSUMO_xy2geo(
        conversionFactor,
        initialGeoCoordinates,
        relativeSUMOPoint):
    return [
        (s * conversionFactor[i]) +
        initialGeoCoordinates[i]
        for i, s in enumerate(relativeSUMOPoint)]


tree = ET.parse('main.net.xml')
root = tree.getroot()

# Retrieve a dictonary (loc_xy) which keys correspond to the name of
# the edges and the values are the relative SUMO map
# location (x,y pair).
# Note: The location of the edge is only considered for one of
# the end, start points of that edge.
loc_xy = {}
for child in root.findall('edge'):
    if(child.attrib.get('shape', [])):
        loc_xy[child.attrib['id']] = [
            (float(child.attrib['shape'].split(' ')[0].split(',')[0]) +
             float(child.attrib['shape'].split(' ')[-1].split(',')[0])) / 2,
            (float(child.attrib['shape'].split(' ')[0].split(',')[1]) +
             float(child.attrib['shape'].split(' ')[-1].split(',')[1])) / 2]

    elif (child.findall('lane')[0].attrib.get('shape', [])):
        shapeParam = child.findall('lane')[0]\
            .attrib.get('shape', []).split(' ')
        loc_xy[child.attrib['id']] = [
            (float(shapeParam[0].split(',')[0]) +
             float(shapeParam[-1].split(',')[0])) / 2,
            (float(shapeParam[0].split(',')[1]) +
             float(shapeParam[-1].split(',')[1])) / 2]

# Information about the relative map location and
# the real latitude and longitude of the points needs
# to be retrived.
# geo_loc_xy is an array that contains the (0,0) position
# with respect to the real latitude and longitude.
# delta_geo_xy is the difference between geo_loc_xy points
# and the opposite corner of the map
# MapLimits correspond to the SUMO relative size of the map
# represented as (x,y pair)

GEO_Y_OFFSET = 0.0003

for child in root.findall('location'):
    # print(child.attrib.get('origBoundary').split(','))
    geo_loc_xy = [
        float(child.attrib.get('origBoundary').split(',')[0]),
        float(child.attrib.get('origBoundary').split(',')[1]) + GEO_Y_OFFSET]
    # delta_geo_xy = [ 0.110373, 0.114781]
    delta_geo_xy = [
        float(child.attrib.get('origBoundary').split(',')[2]) -
        float(child.attrib.get('origBoundary').split(',')[0]),
        float(child.attrib.get('origBoundary').split(',')[3]) -
        float(child.attrib.get('origBoundary').split(',')[1])]
    delta_geo_xy = [abs(s) for s in delta_geo_xy]
    # MapLimits = [11535.26, 12717.13]
    MapLimits = [
        float(child.attrib.get('convBoundary').split(',')[2]),
        float(child.attrib.get('convBoundary').split(',')[3])]
    break

# The following array is the relationship of a SUMO
# (x,y) point into a real latitude, longitude pair
# These values shall be multiplied by the relative
# SUMO (x,y) pair of interest
Conversion_map2geo = [delta_geo_xy[0] / MapLimits[0],
                      delta_geo_xy[1] / MapLimits[1]]


treePoly = ET.parse('main.poly.xml')
rootPoly = treePoly.getroot()

treeNet = ET.parse('main.net.xml')
rootNet = treeNet.getroot()

bikeStations = []

dict_BikeStations = {}

with open('EstacionesMIBICI.txt', 'r') as bikeStationsFile:
    line = bikeStationsFile.readline()
    while line:
        myType, value = line.strip().split(':')
        bikeStations.append(str(value))
        line = bikeStationsFile.readline()


bikeStations_XY = []
for poi in rootPoly.iter('poi'):
    for station in bikeStations:
        if poi.attrib.get('id') == station:
            bikeStations_XY.append([
                float(poi.attrib.get('x')),
                float(poi.attrib.get('y'))])


bikeStationsEdges = []

for curBiSt in bikeStations_XY:
    _, _, mapLimitX, mapLimitY = \
        rootNet.find('location').get('convBoundary').split(',')

    minedgeDistance = \
        GeometryClass.getDistance(
            [0, 0],
            [float(mapLimitX), float(mapLimitY)])

    for edge in rootNet.findall('edge'):
        if(edge.attrib.get('shape') is not None):
            shape = edge.attrib.get('shape').split(' ')
        elif (edge.findall('lane')[0].attrib.get('shape') is not None):
            shape = edge.findall('lane')[0].attrib.get('shape').split(' ')
            # print(shape)
        else:
            raise

        X1, Y1 = shape[0].split(',')
        X1s, Y1s = shape[-1].split(',')

        X1 = (float(X1) + float(X1s)) / 2
        Y1 = (float(Y1) + float(Y1s)) / 2

        tempDistance = \
            GeometryClass.getDistance(
                [float(X1), float(Y1)],
                [float(curBiSt[0]), float(curBiSt[1])])

        if((tempDistance < minedgeDistance) &
                ('cluster' not in edge.attrib.get('id')) &
                (':' not in edge.attrib.get('id'))):

            minedgeDistance = tempDistance
            nearestEdge = edge.attrib.get('id')
    bikeStationsEdges.append(nearestEdge)


stationGeoLocation = []
with open('BikeStationMapping.csv', 'r') as bikeStationMapping:
    line = bikeStationMapping.readline()
    line = bikeStationMapping.readline()
    while line:
        stationMap = line.split(',')
        stationGeoLocation.append([
            int(stationMap[0]),
            [float(stationMap[5]), float(stationMap[4])]])
        line = bikeStationMapping.readline()


bikeStationInfo = {}
for bkSta in bikeStationsEdges:
    minDifference = 100
    for i, geo in stationGeoLocation:
        # print("Station " + str(i) + ' has a location of ' +
        #    str(geo[0]) + ', ' + str(geo[1]))
        dDifference = \
            GeometryClass.getDistance(
                geo,
                relativeSUMO_xy2geo(
                    Conversion_map2geo,
                    geo_loc_xy, loc_xy.get(bkSta, [])))
        # print("Distance from station to poi is: " + str(dDifference))

        if dDifference < minDifference:
            minDifference = dDifference
            minDifference_sID = i
    bikeStationInfo[minDifference_sID] = bkSta
    # print("Neareast station to poi is: " + str(minDifference_sID ))
print(bikeStationInfo)


# In[ ]:
