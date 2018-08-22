function c = myCal(rawdata, gain, offst)
c = (rawdata .* gain) + offst;