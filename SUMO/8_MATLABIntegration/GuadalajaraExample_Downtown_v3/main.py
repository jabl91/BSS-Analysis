#!/usr/bin/env python
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2009-2018 German Aerospace Center (DLR) and others.
# This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v20.html
# SPDX-License-Identifier: EPL-2.0

# @file    _main.py
# @author  Lena Kalleske
# @author  Daniel Krajzewicz
# @author  Michael Behrisch
# @author  Jakob Erdmann
# @author  Alberto Briseno
# @date    2019-08-11
# @version $Id$

from __future__ import absolute_import
from __future__ import print_function
from RouteAnalysis import RouteAnalysis

import os
import sys
import optparse
import random

STEP_SIZE = 0.1

# we need to import python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary  # noqa
import traci  # noqa


def generate_routefile():
    random.seed(42)  # make tests reproducible
    N = 3600  # number of time steps
    # demand per second from different directions
    pWE = 1. / 10
    pEW = 1. / 11
    pNS = 1. / 30
    with open('data/cross.rou.xml', 'w') as routes:
        print("""<routes>
            <vType id="typeWE" accel="0.8" decel="4.5"
            sigma="0.5" length="5" minGap="2.5" maxSpeed="16.67"
            guiShape="passenger"/>
            <vType id="typeNS" accel="0.8" decel="4.5" sigma=
            "0.5" length="7" minGap="3" maxSpeed="25" guiShape="bus"/>

        <route id="right" edges="51o 1i 2o 2oz 52i" />
        <route id="left" edges="52o 2iz 2i 1o 51i" />
        <route id="down" edges="54o 4i 3o 53i" />""", file=routes)
        vehNr = 0
        for i in range(N):
            if random.uniform(0, 1) < pWE:
                print('    <vehicle id="right_%i" type="typeWE" \
                        route="right" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < pEW:
                print('    <vehicle id="left_%i" type="typeWE" \
                        route="left" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < pNS:
                print('    <vehicle id="down_%i" type="typeNS" \
                        route="down" depart="%i" color="1,0,0"/>' % (
                    vehNr, i), file=routes)
                vehNr += 1
        print('</routes>', file=routes)

# The program looks like this
#    <tlLogic id="0" type="static" programID="0" offset="0">
# the locations of the tls are      NESW
#        <phase duration="31" state="GrGr"/>
#        <phase duration="6"  state="yryr"/>
#        <phase duration="31" state="rGrG"/>
#        <phase duration="6"  state="ryry"/>
#    </tlLogic>


def run():
    """execute the TraCI control loop"""
    step = 0

    traci.route.add('myDynamicTrip', ['startEdge', 'endEdge'])
    myRouteAnalysis = RouteAnalysis()

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        step += 1
        if step % (10 / STEP_SIZE) == 0:

            traci.vehicle.add('DynamicVeh_' + str(step),
                              'myDynamicTrip',
                              typeID='bike')
            traci.vehicle.setColor('DynamicVeh_' + str(step),
                                   (0, 0, 255))
            traci.vehicle.setRoutingMode(
                'DynamicVeh_' + str(step),
                traci.constants.ROUTING_MODE_AGGREGATED)
            traci.vehicle.changeTarget('DynamicVeh_' + str(step),
                                       'endEdge')

            traci.vehicle.setParameter('DynamicVeh_' + str(step),
                                       'has.rerouting.device',
                                       'true')

            traci.vehicle.setParameter('DynamicVeh_' + str(step),
                                       'device.rerouting.period',
                                       '30')
        if step % (5 / STEP_SIZE) == 0:
            allActiveVehicles = traci.vehicle.getIDList()
            dynamicVehicles = [s for s in allActiveVehicles
                               if 'DynamicVeh_' in s]

            if dynamicVehicles:
                myRouteAnalysis.convertVehicleLane2VehicleEdge(
                    traci.vehicle.getLaneID(dynamicVehicles[0]))
                # print(traci.edge.getLaneNumber(vehicleEdge))
                # print(360 - traci.vehicle.getAngle(dynamicVehicles[0]))

        if step % (50 / STEP_SIZE) == 0:
            # if dynamicVehicles:
            #    traci.vehicle.changeTarget(dynamicVehicles[0], 'startEdge')

            myCurrentRoutes = traci.route.getIDList()
            if myCurrentRoutes:
                myRouteAnalysis.setCurrentRoute(myCurrentRoutes[0])
                # print(myRouteAnalysis.getCurrentRoute())
                # print(myRouteAnalysis.getAllEdges())
                myRouteAnalysis.RA_mainFunction()

            # print(traci.vehicletype.getIDList())
    traci.close()
    sys.stdout.flush()


def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option('--nogui', action='store_true',
                         default=False,
                         help='run the commandline version of sumo')
    options, args = optParser.parse_args()
    return options


# this is the main entry point of this script
if __name__ == '__main__':
    options = get_options()

    # this script has been called from the command line.
    # It will start sumo as a server, then connect and run
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # first, generate the route file for this simulation
    # generate_routefile()

    # This start a multi client connection, port and client number
    # must be configured

    # traci.start([sumoBinary, '-c', 'osm.sumocfg',
    #                         '--tripinfo-output', 'output/tripinfo.xml',
    #                         '--num-clients', '2'], port=58890)

    # This is the normal way of using traci. sumo is started as a
    # subprocess and then the python script connects and runs

    traci.start([sumoBinary, '-c', 'main.sumocfg',
                             '--tripinfo-output', 'output/tripinfo.xml'])

    # Support for MultiClient TraCI Requests
    traci.setOrder(1)

    run()
