python "%SUMO_HOME%\tools\randomTrips.py" -n osm.net.xml --seed 42 --fringe-factor 1.200000 -p 0.509470 -r osm.passenger.rou.xml -o osm.passenger.trips.xml -e 3600 --vehicle-class passenger --vclass passenger --prefix veh --min-distance 300 --trip-attributes "departLane=\"best\"" --validate
