
import pandas as pd
import numpy as np
from NvMAccelerator import NvMAccelerator


class BikeRelocationScheme:

    # constants
    C_MESSAGES = False
    C_WEIGHTINDEX = 2

    # attributes
    BikeRelocationScheme = {}

    def __init__(
            self,
            StationsArray,
            NumberofDocks_Station=15):
        for NumeroEstacion in StationsArray:

            try:
                myData = NvMAccelerator.pickled_items(
                    './test/' +
                    'RebalancingStation' + str(NumeroEstacion) + '.pkl')

                for element in myData:
                    self.BikeRelocationScheme[NumeroEstacion] =\
                        element
                    break
                if(self.C_MESSAGES is True):
                    print(
                        'Bike Relocation for Station ' +
                        str(NumeroEstacion) +
                        ' loaded.')

            except:

                # Load the Pandas libraries with alias 'pd'
                # import pandas as pd
                # Read data from file 'filename.csv'
                # (in the same directory that your python process is based)
                # Control delimiters, rows, column names with read_csv
                # (see later)
                data2 = pd.read_csv(
                    './test/' + 'InfoStation' + str(NumeroEstacion) + '.csv')

                # Preview the first 5 lines of the loaded data
                # data2.head()
                # data2

                # Values have been sorted by appareance order
                data2.sort_values(
                    'Viaje_Id', axis=0, ascending=True,
                    inplace=True, na_position='last')

                # convert the 'Date' column to datetime format
                data2['Inicio_del_viaje'] =\
                    pd.to_datetime(data2['Inicio_del_viaje'])

                # Check the format of 'Date' column
                # OutGoingTrips.info()

                # convert the 'Date' column to datetime format
                data2['Fin_del_viaje'] =\
                    pd.to_datetime(data2['Fin_del_viaje'])

                # Check the format of 'Date' column
                # data.info();
                # data

                # It is neccesary to order the timing events based
                # on the type of bike event
                # This means, if the bike is leaving the station,
                # the time to be used
                # corresponds to the time the bike left the station,
                # but if a bike
                # is been docked, then the time that has to be
                # considered is the time
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

                AllTrips_Station_2 =\
                    data2[
                        (data2.Origen_Id == NumeroEstacion) |
                        (data2.Destino_Id == NumeroEstacion)]
                # AllTrips_Station10

                # Optimization performed taking the same weekday along a year

                DayOfTheWeek = 1
                SameDaysinYear = np.arange(DayOfTheWeek, 365, 7)
                SameDaysinYear

                OptimizationWeek = []
                days = [
                    'Monday', 'Tuesday', 'Wednesday',
                    'Thursday', 'Friday', 'Saturday', 'Sunday']
                PlotDay = 124

                for dayofweek in days:
                    OptimizationWeekDay = []
                    SameDaysinYear = np.arange(1, 365, 1)

                    # Percentage 0 to 100 #Final State of the Bike
                    # Station after Rebal event
                    Rebal_Percent = np.arange(0, 100, 10)
                    # Percentage 0.00 to 0.50 #When should the
                    # relocation team approach the station
                    Threshold_Action = 0.10

                    for DayinYear in SameDaysinYear:

                        SingleDayTrips_Station = \
                            AllTrips_Station_2[
                                AllTrips_Station_2['Inicio_del_viaje']
                                .dt.dayofyear == DayinYear]

                        try:
                            DayName = \
                                SingleDayTrips_Station[
                                    'Inicio_del_viaje'].iloc[0].day_name()
                        except:
                            continue

                        if(DayName == dayofweek):

                            # SingleDayTrips_Station

                            ResultsOptimization = []

                            if(DayinYear == PlotDay):
                                PlotBikeStationEvents = []

                            for cur_RebalPerc in Rebal_Percent:

                                OptimizationBadEvents = 0
                                NumberOfBikes = \
                                    int((
                                        cur_RebalPerc *
                                        NumberofDocks_Station) / 100)

                                for _, i in \
                                        SingleDayTrips_Station.iterrows():
                                    if(
                                        (i['Origen_Id'] ==
                                            NumeroEstacion) &
                                        (i['Destino_Id'] !=
                                            NumeroEstacion)):
                                        NumberOfBikes -= 1

                                    elif(
                                        (i['Destino_Id'] ==
                                            NumeroEstacion) &
                                        (i['Origen_Id'] !=
                                            NumeroEstacion)):
                                        NumberOfBikes += 1
                                    else:
                                        # print("Algo anda mal")
                                        # print(i['Origen_Id'])
                                        # print(i['Destino_Id'])
                                        break
                                    if((NumberOfBikes <=
                                            int(
                                                (Threshold_Action) *
                                                NumberofDocks_Station)) |
                                        (NumberOfBikes >=
                                            int((1 - Threshold_Action) *
                                                NumberofDocks_Station))):
                                        # print("Camioncito de relocacion")
                                        # print("Dejando la estacion al " +
                                        # str(cur_RebalPerc) + "%")
                                        NumberOfBikes = \
                                            int((
                                                cur_RebalPerc *
                                                NumberofDocks_Station) / 100)
                                        OptimizationBadEvents += 1
                                    # else:
                                        # print("All is gut " +
                                        # str(NumberOfBikes))
                                    if(DayinYear == PlotDay):
                                        PlotBikeStationEvents.append(
                                            NumberOfBikes)
                                ResultsOptimization.append(
                                    [cur_RebalPerc, OptimizationBadEvents])
                            # print(ResultsOptimization)

                            Percentage = ResultsOptimization[0][0]
                            MinNumberofBadEvents = ResultsOptimization[0][1]
                            SameEvents = []
                            SameEventPercentages = []
                            for i, badevents in ResultsOptimization:
                                if(MinNumberofBadEvents >= badevents):
                                    MinNumberofBadEvents = badevents
                                    Percentage = i
                                    if(len(SameEvents) != 0):
                                        if(SameEvents[-1] == badevents):
                                            SameEvents.append(badevents)
                                            SameEventPercentages.append(i)
                                        else:
                                            SameEvents = [badevents]
                                            SameEventPercentages = [i]
                                    else:
                                        SameEvents.append(badevents)
                                        SameEventPercentages.append(i)

                            Average = 0
                            for per in SameEventPercentages:
                                Average += per
                            if(len(SameEventPercentages) != 0):
                                Average = Average / len(SameEventPercentages)
                            # print("The optimal percentage of bikes to
                            # start is: "+ str(Percentage))
                            # print("The number of relocations needed
                            # were:", MinNumberofBadEvents)

                            # OptimizationWeekDay Description:

                            # [0]DayinYear corresponds to Monday, Tuesday,
                            # Wednesday, etc
                            # [1]SameEventPercentages is an array with all
                            # the percentages that matched the
                            # MinNumberofBadEvents
                            # [2]Average is the average of all the
                            # elements in SameEventPercentages
                            # [3]Percentage is the maximum of
                            # SameEvent Percentages
                            # [4]MinNumberofBadEvents is the minimum number
                            # of bike relocation events for every
                            # element of rebalancing
                            # percentages on SameEventPercentages

                            OptimizationWeekDay.append([
                                DayinYear, SameEventPercentages,
                                Average, Percentage,
                                MinNumberofBadEvents, DayName])

                    OptimizationWeek.append(OptimizationWeekDay)

                AverageInfo = []
                for optim_day in OptimizationWeek:
                    AveragePerforAllSameDay = 0
                    AverageRelocations = 0
                    for element in optim_day:
                        AveragePerforAllSameDay += element[2]
                        AverageRelocations += element[-2]

                    if(len(OptimizationWeekDay) != 0):
                        AveragePerforAllSameDay /= len(OptimizationWeekDay)
                        AverageRelocations /= len(OptimizationWeekDay)

                    print(
                        optim_day[0][-1] +
                        ': ' +
                        'AverageRelocYear: ' +
                        str(AverageRelocations))
                    print(
                        'Relocation Average per event: ' +
                        str(AveragePerforAllSameDay))
                    print()

                    AverageInfo.append([
                        optim_day[0][-1], AverageRelocations,
                        AveragePerforAllSameDay, NumeroEstacion])

                self.BikeRelocationScheme[NumeroEstacion] =\
                    AverageInfo

                NvMAccelerator.save_object(
                    AverageInfo,
                    './test/' +
                    'RebalancingStation' + str(NumeroEstacion) + '.pkl')

                print('Station Analyzed: ' + str(NumeroEstacion))

    def getRebalancingWeights(self):
        return self.BikeRelocationScheme


# StationNumber = 2
# WkdDay = 6
# myBikeRelocationScheme = BikeRelocationScheme([StationNumber])
# print(myBikeRelocationScheme.getRebalancingWeights()[StationNumber][WkdDay])
