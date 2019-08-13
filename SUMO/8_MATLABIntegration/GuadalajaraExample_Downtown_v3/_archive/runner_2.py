#!/usr/bin/env python
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2009-2018 German Aerospace Center (DLR) and others.
# This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v20.html
# SPDX-License-Identifier: EPL-2.0

# @file    runner.py
# @author  Lena Kalleske
# @author  Daniel Krajzewicz
# @author  Michael Behrisch
# @author  Jakob Erdmann
# @author  Alberto Briseno
# @date    2019-01-11
# @version $Id$

from __future__ import absolute_import
from __future__ import print_function

import os
import sys

STEP_SIZE = 0.1

# we need to import python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary  # noqa
import traci  # noqa


def run():
    """execute the TraCI control loop"""
    step = 0

    traci.route.add('myDynamicTrip2', ['startEdge', 'endEdge'])
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        step += 1
        if step % (100/STEP_SIZE) == 0:
            traci.vehicle.add('DynamicVeh2_' + str(step),
                              'myDynamicTrip2',
                              typeID='DEFAULT_VEHTYPE')
            traci.vehicle.setColor('DynamicVeh2_' + str(step),
                                   (0, 255, 0))
        if step % (25/STEP_SIZE) == 0:
            allActiveVehicles = traci.vehicle.getIDList()
            dynamicVehicles = [s for s in allActiveVehicles
                               if 'DynamicVeh2_' in s]
            if dynamicVehicles:
                print(dynamicVehicles)
    traci.close()
    sys.stdout.flush()


# this is the main entry point of this script
if __name__ == '__main__':

    traci.init(58890)
    # Support for MultiClient TraCI Requests
    traci.setOrder(2)

    run()
