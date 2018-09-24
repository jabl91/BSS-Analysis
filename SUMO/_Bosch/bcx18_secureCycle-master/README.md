# Bosch ConnectedExperience 2018 - Hack Challenge #2: Autonomous Driving

This demo was made with SUMO and the help of the nice hack coaches of
the German Aerospace Center (DLR). Thanks again for your support!

## Prerequisites

### Get and install SUMO

 See https://github.com/DLR-TS/sumo

### Make SUMO Python libraries known
``
export PYTHONPATH=${SUMO_DIR}/tools
``

## Running the demo

### Using the default model
``
./secure_cycle.py
``

### Using the secure cycle model
``
./secure_cycle.py save_cyclists
``

#### Added features:
* cars do not overtake cyclists if the lane width is smaller than 4.0 meters
* driver feedback if it is not safe to overtake cyclists
* driver feedback for how long it is safe to overtake cyclists
