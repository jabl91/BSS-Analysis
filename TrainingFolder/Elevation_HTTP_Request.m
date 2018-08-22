%clear all;
%clc;

import matlab.net.*
import matlab.net.http.*

r = RequestMessage;

[DataSize,~] = size(Elevation_PreHTTPRequest)

for i = 1:DataSize

    latitud =    num2str(Elevation_PreHTTPRequest(i,2),10);
    longitud =    num2str(Elevation_PreHTTPRequest(i,3),10);
    coord = latitud + "," + longitud;
    base_Req = "https://maps.googleapis.com/maps/api/elevation/json?locations=";

    uri = URI(base_Req + coord);
    resp = send(r,uri);
    status = resp.StatusCode
    "Numero de Peticion"
    i

    if status == 'OK' 

       Elevation_PreHTTPRequest(i,4) = resp.Body.Data.results.elevation;

    else

       Elevation_PreHTTPRequest(i,4) = 0;

    end
end