# Standard data science
import pandas as pd
import numpy as np
# from scipy.special import factorial
# from scipy.io import loadmat
# Import required library to generate pseudo-random numbers
import random

np.random.seed(42)

# Load the Pandas libraries with alias 'pd'
# import pandas as pd
# Read data from file 'filename.csv'
# (in the same directory that your python process is based)
# Control delimiters, rows, column names with read_csv (see later)
NumeroEstacion = 10
NumberofDocks_Station10 = 15

# data2 = pd.read_csv('InfoStation' + str(NumeroEstacion) + '.csv')
data2 = pd.read_csv('./test/InfoStation10.csv')

# Preview the first 5 lines of the loaded data
# data2.head()
# data2

# Values have been sorted by appareance order
data2.sort_values(
    'Viaje_Id', axis=0, ascending=True,
    inplace=True, na_position='last')

# convert the 'Date' column to datetime format
data2['Inicio_del_viaje'] = \
    pd.to_datetime(data2['Inicio_del_viaje'])

# Check the format of 'Date' column
# OutGoingTrips.info()

# convert the 'Date' column to datetime format
data2['Fin_del_viaje'] =\
    pd.to_datetime(data2['Fin_del_viaje'])

# Check the format of 'Date' column
# data.info();
# data

# It is neccesary to order the timing events based on the type of bike event
# This means, if the bike is leaving the station, the time to be used
# corresponds to the time the bike left the station, but if a bike
# is been docked, then the time that has to be considered is the time
# the bike arrive to the station

OrderedTimeEvents = []
for _, row in data2.iterrows():
    if((row['Origen_Id'] == NumeroEstacion) &
            (row['Destino_Id'] != NumeroEstacion)):
        OrderedTimeEvents.append(row['Inicio_del_viaje'])

    elif((row['Destino_Id'] == NumeroEstacion) &
            (row['Origen_Id'] != NumeroEstacion)):
        OrderedTimeEvents.append(row['Fin_del_viaje'])

    else:
        print('Origen y Destino iguales')
        raise

# OrderedTimeEvents

# A new column will be created on the main table
# that contains this information
data2['EventosTiempoEstacion'] = OrderedTimeEvents
# data2.head()


# And now the events should be sorted by the new column created
# this events would now allow the optimization problem to
# find the best solution

data2.sort_values(
    'EventosTiempoEstacion', axis=0, ascending=True,
    inplace=True, na_position='last')
# data2

# OutGoingTrips = data[data.Origen_Id == 10]
# OutGoingTrips
# InboundTrips = data[data.Destino_Id == 10]
# InboundTrips

stationDepartures = data2[(data2.Origen_Id == NumeroEstacion)]
stationArrivals = data2[(data2.Destino_Id == NumeroEstacion)]
# AllTrips_Station10


def computeCDF(n, bins):
    integral = []
    bin_width = bins[1] - bins[0]

    for i, _ in enumerate(n):
        integral.append(bin_width * sum(n[0:i]))

    return integral


def convertSeriesTime2Seconds(time):
    seconds = time.hour.values * 3600
    seconds += time.minute.values * 60
    seconds += time.second.values
    return seconds


# Pandas DataFrame for all departures within every
# same day of the week. Index 0 -> Monday, ...
# Index 6 -> Sunday.
wkDayDepartures = []

# Histogram of all departures time within evey
# same day of the week.
# Note: Departures time correspond to seconds
# 24(hours)*3600(seconds) is the maximum value
# expected.
# Index 0 -> Monday, ...
# Index 6 -> Sunday.
wkDayDepartures_hist = []

# Cumulative distributive function of all departures
# time within every same day of the week.
# Note: Departures time correspond to seconds
# 24(hours)*3600(seconds) is the maximum value
# expected.
# Index 0 -> Monday, ...
# Index 6 -> Sunday.
wkDayDepartures_cdf = []

# List of total number departure trips within
# every same day of the week.
# Index 0 -> Monday, ...
# Index 6 -> Sunday.
numTripsInDay = []

# Cumulative distributive function of total number
# departure trips within every same day of the week.
# Note: Departures time correspond to seconds
# 24(hours)*3600(seconds) is the maximum value
# expected.
# Index 0 -> Monday, ...
# Index 6 -> Sunday.
numTripsInDay_cdf = []

for weekday in range(7):
    weekdayData = stationDepartures[
        stationDepartures['Inicio_del_viaje']
        .dt.dayofweek == weekday]

    wkDayDepartures.append(weekdayData)

    myhistData = \
        convertSeriesTime2Seconds(weekdayData.Inicio_del_viaje.dt)

    hist, bin_edges = \
        np.histogram(
            myhistData, bins=24 * 8,
            density=True,
            range=(0.0, 24.0 * 3600))

    hist = np.append(hist, [0.0])

    wkDayDepartures_hist.append([hist, bin_edges])

    wkDayDepartures_cdf.append([bin_edges, computeCDF(hist, bin_edges)])

    myDict = {}
    [myDict.setdefault(s.dayofyear, 0) for s in
        list(weekdayData.Inicio_del_viaje)]

    daysDatabase = list(myDict.keys())

    tempTripsinDay = []
    for day in daysDatabase:
        tripsInDay = \
            weekdayData[
                weekdayData['Inicio_del_viaje']
                .dt.dayofyear == day]

        tempTripsinDay.append(len(tripsInDay))

    numTripsInDay.append(tempTripsinDay)

    hist2, bin_edges2 = \
        np.histogram(
            tempTripsinDay, bins=50,
            density=True,
            range=(0.0, 100.0))
    hist2 = np.append(hist2, [0.0])

    numTripsInDay_cdf.append([bin_edges2, computeCDF(hist2, bin_edges2)])


# for i in range(7):
#     print(
#         'Mean of trips for day: ' + str(i) + ' is: ' +
#         str(np.mean(numTripsInDay[i])))
#     lines = plt.plot(
#         numTripsInDay_cdf[i][0], numTripsInDay_cdf[i][1])
# plt.legend([
#     'Monday', 'Tuesday',
#     'Wednesday', 'Thursday',
#     'Friday', 'Saturday', 'Sunday'])

def getRndmNumberOfCDF(wkday, myCDF):
    myRandNum = random.randint(1, 1000)
    for j, e in enumerate(myCDF[wkday][1]):
        if(myRandNum <= (e * 1000)):
            break
    return myCDF[wkday][0][j]


tripTimestamps = []
for trip in range(int(getRndmNumberOfCDF(0, numTripsInDay_cdf))):
    tripTimestamps.append(getRndmNumberOfCDF(0, wkDayDepartures_cdf) / 3600)
print(len(tripTimestamps))
print(tripTimestamps)
# plt.hist(tripTimestamps, bins='auto')
