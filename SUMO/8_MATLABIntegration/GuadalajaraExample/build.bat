python "%SUMO_HOME%\tools\randomTrips.py" -n osm.net.xml --seed 42 --fringe-factor 2 -p 17.846233 -r osm.bicycle.rou.xml -o osm.bicycle.trips.xml -e 3600 --vehicle-class bicycle --vclass bicycle --prefix bike --max-distance 8000 --trip-attributes "departLane=\"best\"" --validate
