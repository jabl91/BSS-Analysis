%clear all;
%clc;

import matlab.net.*
import matlab.net.http.*

r = RequestMessage;

[DataSize,~] = size(PreHTTPRequest)

for i = 2462:DataSize

    origin_lat =    num2str(PreHTTPRequest(i,3),10);
    origin_lng =    num2str(PreHTTPRequest(i,4),10);
    dest_lat =      num2str(PreHTTPRequest(i,6),10);
    dest_lng =      num2str(PreHTTPRequest(i,7),10);
    origin_coord = origin_lat + "," + origin_lng;
    dest_coord = dest_lat + "," + dest_lng;
    base_Req = "https://maps.googleapis.com/maps/api/directions/json?origin=";
    dest_tag = "&destination=";
    mode = "&mode=bycicling";

    uri = URI(base_Req + origin_coord + dest_tag + dest_coord + mode);
    resp = send(r,uri);
    status = resp.StatusCode
    "Numero de Peticion"
    i

    if status == 'OK' 

       PreHTTPRequest(i,9) = resp.Body.Data.routes.legs.distance.value;
       PreHTTPRequest(i,10) = resp.Body.Data.routes.legs.duration.value;

    else

       PreHTTPRequest(i,9) = 0;
       PreHTTPRequest(i,10) = 0;

    end
end