# Standard data science
# Load the Pandas libraries with alias 'pd'
import pandas as pd
import numpy as np
# from scipy.special import factorial
# from scipy.io import loadmat
# Import required library to generate pseudo-random numbers
import random


class BikeStationCDF:

    # attributes
    NumeroEstacion = 255
    stationDepartures = []
    stationArrivals = []

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

    def __init__(self, stationID):
        np.random.seed(42)
        self.NumeroEstacion = stationID

        # Read data from file 'filename.csv'
        # (in the same directory that your python process is based)
        # Control delimiters, rows, column names with read_csv (see later)

        data2 = pd.read_csv('./test/InfoStation10.csv')

        # Values have been sorted by appareance order
        data2.sort_values(
            'Viaje_Id', axis=0, ascending=True,
            inplace=True, na_position='last')

        # convert the 'Date' column to datetime format
        data2['Inicio_del_viaje'] = \
            pd.to_datetime(data2['Inicio_del_viaje'])

        # convert the 'Date' column to datetime format
        data2['Fin_del_viaje'] =\
            pd.to_datetime(data2['Fin_del_viaje'])

        # It is neccesary to order the timing events
        # based on the type of bike event
        # this means, if the bike is leaving the station, the time to be used
        # corresponds to the time the bike left the station, but if a bike
        # is been docked, then the time that has to be considered is the time
        # the bike arrive to the station

        OrderedTimeEvents = []
        for _, row in data2.iterrows():
            if((row['Origen_Id'] == self.NumeroEstacion) &
                    (row['Destino_Id'] != self.NumeroEstacion)):
                OrderedTimeEvents.append(row['Inicio_del_viaje'])

            elif((row['Destino_Id'] == self.NumeroEstacion) &
                    (row['Origen_Id'] != self.NumeroEstacion)):
                OrderedTimeEvents.append(row['Fin_del_viaje'])

            else:
                print('Origen y Destino iguales')
                raise

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

        self.stationDepartures =\
            data2[(data2.Origen_Id == self.NumeroEstacion)]
        self.stationArrivals =\
            data2[(data2.Destino_Id == self.NumeroEstacion)]

        self._processData()

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

    def getStationId(self):
        return self.NumeroEstacion

    def _processData(self):

        # Pandas DataFrame for all departures within every
        # same day of the week. Index 0 -> Monday, ...
        # Index 6 -> Sunday.
        self.wkDayDepartures = []

        # Histogram of all departures time within evey
        # same day of the week.
        # Note: Departures time correspond to seconds
        # 24(hours)*3600(seconds) is the maximum value
        # expected.
        # Index 0 -> Monday, ...
        # Index 6 -> Sunday.
        self.wkDayDepartures_hist = []

        # Cumulative distributive function of all departures
        # time within every same day of the week.
        # Note: Departures time correspond to seconds
        # 24(hours)*3600(seconds) is the maximum value
        # expected.
        # Index 0 -> Monday, ...
        # Index 6 -> Sunday.
        self.wkDayDepartures_cdf = []

        # List of total number departure trips within
        # every same day of the week.
        # Index 0 -> Monday, ...
        # Index 6 -> Sunday.
        self.numTripsInDay = []

        # Cumulative distributive function of total number
        # departure trips within every same day of the week.
        # Note: Departures time correspond to seconds
        # 24(hours)*3600(seconds) is the maximum value
        # expected.
        # Index 0 -> Monday, ...
        # Index 6 -> Sunday.
        self.numTripsInDay_cdf = []

        for weekday in range(7):
            weekdayData = self.stationDepartures[
                self.stationDepartures['Inicio_del_viaje']
                .dt.dayofweek == weekday]

            self.wkDayDepartures.append(weekdayData)

            myhistData = \
                BikeStationCDF.convertSeriesTime2Seconds(
                    weekdayData.Inicio_del_viaje.dt)

            hist, bin_edges = \
                np.histogram(
                    myhistData, bins=24 * 8,
                    density=True,
                    range=(0.0, 24.0 * 3600))

            hist = np.append(hist, [0.0])

            self.wkDayDepartures_hist.append([hist, bin_edges])

            self.wkDayDepartures_cdf.append(
                [bin_edges, BikeStationCDF.computeCDF(hist, bin_edges)])

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

            self.numTripsInDay.append(tempTripsinDay)

            hist2, bin_edges2 = \
                np.histogram(
                    tempTripsinDay, bins=50,
                    density=True,
                    range=(0.0, 100.0))
            hist2 = np.append(hist2, [0.0])

            self.numTripsInDay_cdf.append(
                [bin_edges2, BikeStationCDF.computeCDF(hist2, bin_edges2)])

    def getRndmNumberOfCDF(wkday, myCDF):
        myRandNum = random.randint(1, 1000)
        for j, e in enumerate(myCDF[wkday][1]):
            if(myRandNum <= (e * 1000)):
                break
        return myCDF[wkday][0][j]

    def getCDFTripsPerDay(self, wkday):
        tripTimestamps = []

        for trip in range(
                int(BikeStationCDF.getRndmNumberOfCDF(
                    wkday, self.numTripsInDay_cdf))):
            tripTimestamps.append(
                BikeStationCDF.getRndmNumberOfCDF(
                    wkday, self.wkDayDepartures_cdf) / 3600)

        # print(len(tripTimestamps))
        # print(tripTimestamps)
        return tripTimestamps
        # plt.hist(tripTimestamps, bins='auto')


myBikeStationCDF = BikeStationCDF(10)
print(np.sort(myBikeStationCDF.getCDFTripsPerDay(0)))
