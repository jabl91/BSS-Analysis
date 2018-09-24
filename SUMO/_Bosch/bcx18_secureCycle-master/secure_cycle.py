#!/bin/env python3

# Copyright 2018, Steffen Pankratz
# SPDX-License-Identifier: BSD-3-Clause

import sys

import sumolib
import traci

SAFE_LANE_MIN_WIDTH = 10.0


class BikeListener(traci.StepListener):
    def __init__(self):
        self.car_ids = list()

    def step(self, s=0):
        _ = s
        for veh in traci.simulation.getDepartedIDList():
            if traci.vehicle.getTypeID(veh) == 'Car':
                self.car_ids.append(veh)
        for veh in traci.simulation.getArrivedIDList():
            if veh in self.car_ids:
                self.car_ids.remove(veh)
        for car_id in self.car_ids:
            leader_info = traci.vehicle.getLeader(car_id)
            if leader_info and is_bike(leader_info[0]):
                set_lane_change_mode(car_id)
                set_passing_state(car_id)


def is_bike(vehicle_id):
    return traci.vehicle.getTypeID(vehicle_id) == 'Bike'


def set_passing_state(car_id):
    lane = traci.vehicle.getLaneID(car_id)
    assert lane
    lane_len = traci.lane.getLength(lane)
    lane_offset = traci.vehicle.getLanePosition(car_id)
    lane_end_in = lane_len - lane_offset
    if traci.lane.getWidth(lane) > SAFE_LANE_MIN_WIDTH:
        print('Save to pass cyclist in the next %s meters' % lane_end_in)
    else:
        print('NOT save to pass cyclist!')
        next_lane = traci.vehicle.getBestLanes(car_id)[0][5][1]
        if traci.lane.getWidth(next_lane) > SAFE_LANE_MIN_WIDTH:
            print('\tBut save in %s meters' % lane_end_in)


def set_lane_change_mode(car_id):
    lane = traci.vehicle.getLaneID(car_id)
    assert lane
    if traci.lane.getWidth(lane) > SAFE_LANE_MIN_WIDTH:
        traci.vehicle.setLaneChangeMode(car_id, 0b011001010101)
    else:
        traci.vehicle.setLaneChangeMode(car_id, 0b011001000000)


def run():
    step = 0
    sumo_binary = sumolib.checkBinary('sumo-gui')
    traci.start([sumo_binary, '-c', 'testcase_01.sumocfg',
                 '--lateral-resolution', '0.5', '-S', '-Q'])
    print(sys.argv)
    if len(sys.argv) >= 2 and sys.argv[1] == 'save_cyclists':
        listener = BikeListener()
        traci.addStepListener(listener)
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        step += 1
        print(step)
    traci.close()


if __name__ == '__main__':
    run()
