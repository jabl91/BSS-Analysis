#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Standard data science
import pandas as pd
import numpy as np

np.random.seed(42)

# Display all cell outputs
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = 'all'

# Visualizations
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import iplot

# Cufflinks for dataframes
import cufflinks as cf
cf.go_offline()
cf.set_config_file(world_readable=True, theme='pearl')

from scipy.special import factorial

from scipy.io import loadmat


# In[2]:


# Load the Pandas libraries with alias 'pd' 
# import pandas as pd 
# Read data from file 'filename.csv' 
# (in the same directory that your python process is based)
# Control delimiters, rows, column names with read_csv (see later) 
NumeroEstacion = 32
data = pd.read_csv("InfoStation"+str(NumeroEstacion)+".csv")
# Preview the first 5 lines of the loaded data 
data.head()
data


# In[3]:


#Values have been sorted by appareance order
data.sort_values("Viaje_Id", axis = 0, ascending= True, 
                 inplace = True, na_position ='last')

# convert the 'Date' column to datetime format 
data['Inicio_del_viaje']= pd.to_datetime(data['Inicio_del_viaje']);
  
# Check the format of 'Date' column 
# OutGoingTrips.info()

# convert the 'Date' column to datetime format 
data['Fin_del_viaje']= pd.to_datetime(data['Fin_del_viaje']);
  
# Check the format of 'Date' column 
#data.info();
#data


# In[4]:


#OutGoingTrips = data[data.Origen_Id == 10]
#OutGoingTrips
#InboundTrips = data[data.Destino_Id == 10]
#InboundTrips

AllTrips_Station10 = data[(data.Origen_Id == NumeroEstacion) | (data.Destino_Id == NumeroEstacion)]
#AllTrips_Station10


# In[5]:



#Optimization performed taking the same weekday along a year

DayOfTheWeek = 1
DayOfTheYear = 75
SameDaysinYear = np.arange(DayOfTheWeek,365,7)
SameDaysinYear


# In[6]:



OptimizationWeekDay = []

#Percentage 0 to 100 #Final State of the Bike Station after Rebal event
Rebal_Percent = np.arange(0,100,10); 
#Percentage 0.00 to 0.50 #When should the relocation team approach the station
Threshold_Action = 0.10; 

NumberofDocks_Station10 = 15

for DayinYear in SameDaysinYear:

    SingleDayTrips_Station10 =         AllTrips_Station10[AllTrips_Station10['Inicio_del_viaje'].dt.dayofyear == DayinYear]

    #SingleDayTrips_Station10
    
    ResultsOptimization = []

    for cur_RebalPerc in Rebal_Percent:

        OptimizationBadEvents = 0
        NumberOfBikes = int((cur_RebalPerc*NumberofDocks_Station10)/100)

        for _, i in SingleDayTrips_Station10.iterrows():
            if((i['Origen_Id'] == NumeroEstacion) & (i['Destino_Id'] != NumeroEstacion)):
                NumberOfBikes-=1;
            elif((i['Destino_Id'] == NumeroEstacion) & (i['Origen_Id'] != NumeroEstacion)):
                NumberOfBikes+=1
            else:
                print("Algo anda mal")
                print(i['Origen_Id'])
                print(i['Destino_Id'])
                break
            if((NumberOfBikes < int( (Threshold_Action) * NumberofDocks_Station10 )) |                 (NumberOfBikes > int( (1-Threshold_Action) * NumberofDocks_Station10 ))):
                #print("Camioncito de relocacion")
                #print("Dejando la estacion al " + str(cur_RebalPerc) + "%")
                NumberOfBikes = int((cur_RebalPerc*NumberofDocks_Station10) / 100)
                OptimizationBadEvents+= 1
            #else:
                #print("All is gut " + str(NumberOfBikes))

        ResultsOptimization.append([cur_RebalPerc, OptimizationBadEvents])
    #print(ResultsOptimization)

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
    #print("The optimal percentage of bikes to start is: "+ str(Percentage))
    #print("The number of relocations needed were:", MinNumberofBadEvents)

    #OptimizationWeekDay Description:
    
    #[0]DayinYear corresponds to Monday, Tuesday, Wednesday, etc
    #[1]SameEventPercentages is an array with all the percentages that matched the MinNumberofBadEvents
    #[2]Average is the average of all the elements in SameEventPercentages
    #[3]Percentage is the maximum of SameEvent Percentages
    #[4]MinNumberofBadEvents is the minimum number of bike relocation events for every element of rebalancing
    #    percentages on SameEventPercentages
    
    OptimizationWeekDay.append([DayinYear,SameEventPercentages,Average,Percentage,MinNumberofBadEvents])

OptimizationWeekDay


# In[7]:


AveragePerforAllSameDay = 0
for element in OptimizationWeekDay:
    AveragePerforAllSameDay += element[2]

if(len(OptimizationWeekDay) != 0):
    AveragePerforAllSameDay /= len(OptimizationWeekDay)

AveragePerforAllSameDay


# In[8]:


# Load the Pandas libraries with alias 'pd' 
# import pandas as pd 
# Read data from file 'filename.csv' 
# (in the same directory that your python process is based)
# Control delimiters, rows, column names with read_csv (see later) 
data2 = pd.read_csv("InfoStation"+str(NumeroEstacion)+".csv")

# Preview the first 5 lines of the loaded data 
data2.head()
#data2


# In[9]:


#Values have been sorted by appareance order
data2.sort_values("Viaje_Id", axis = 0, ascending= True, 
                 inplace = True, na_position ='last')

# convert the 'Date' column to datetime format 
data2['Inicio_del_viaje']= pd.to_datetime(data2['Inicio_del_viaje']);
  
# Check the format of 'Date' column 
# OutGoingTrips.info()

# convert the 'Date' column to datetime format 
data2['Fin_del_viaje']= pd.to_datetime(data2['Fin_del_viaje']);
  
# Check the format of 'Date' column 
#data.info();
#data


# In[10]:


#It is neccesary to order the timing events based on the type of bike event
#This means, if the bike is leaving the station, the time to be used
#corresponds to the time the bike left the station, but if a bike
#is been docked, then the time that has to be considered is the time
#the bike arrive to the station

OrderedTimeEvents = []
for _, row in data2.iterrows():
    if((row['Origen_Id'] == NumeroEstacion) & (row['Destino_Id'] != NumeroEstacion)):
        OrderedTimeEvents.append(row['Inicio_del_viaje'])
    elif((row['Destino_Id'] == NumeroEstacion) & (row['Origen_Id'] != NumeroEstacion)):
        OrderedTimeEvents.append(row['Fin_del_viaje'])
    else:
        print("Origen y Destino iguales")
        
#OrderedTimeEvents

#A new column will be created on the main table that contains this information
data2['EventosTiempoEstacion'] = OrderedTimeEvents
data2.head()


# In[11]:


#And now the events should be sorted by the new column created
#this events would now allow the optimization problem to
#find the best solution

data2.sort_values('EventosTiempoEstacion', axis = 0, ascending= True, 
                 inplace = True, na_position ='last')
#data2


# In[12]:


#OutGoingTrips = data[data.Origen_Id == 10]
#OutGoingTrips
#InboundTrips = data[data.Destino_Id == 10]
#InboundTrips

AllTrips_Station10_2 = data2[(data2.Origen_Id == NumeroEstacion) | (data2.Destino_Id == NumeroEstacion)]
#AllTrips_Station10


# In[13]:



#Optimization performed taking the same weekday along a year

DayOfTheWeek = 1
DayOfTheYear = 75
SameDaysinYear = np.arange(DayOfTheWeek,365,7)
SameDaysinYear


# In[ ]:


OptimizationWeek = []
days = np.arange(1,8,1)

for dayofweek in days:
    OptimizationWeekDay = []
    SameDaysinYear = np.arange(dayofweek,365,7)
    
    #Percentage 0 to 100 #Final State of the Bike Station after Rebal event
    Rebal_Percent = np.arange(0,100,10); 
    #Percentage 0.00 to 0.50 #When should the relocation team approach the station
    Threshold_Action = 0.10; 

    NumberofDocks_Station10 = 15

    for DayinYear in SameDaysinYear:

        SingleDayTrips_Station10 =             AllTrips_Station10_2[AllTrips_Station10_2['Inicio_del_viaje'].dt.dayofyear == DayinYear]

        #SingleDayTrips_Station10

        ResultsOptimization = []
        
        DayName = SingleDayTrips_Station10['Inicio_del_viaje'].iloc[0].day_name()

        for cur_RebalPerc in Rebal_Percent:

            OptimizationBadEvents = 0
            NumberOfBikes = int((cur_RebalPerc*NumberofDocks_Station10)/100)

            for _, i in SingleDayTrips_Station10.iterrows():
                if((i['Origen_Id'] == NumeroEstacion) & (i['Destino_Id'] != NumeroEstacion)):
                    NumberOfBikes-=1;
                elif((i['Destino_Id'] == NumeroEstacion) & (i['Origen_Id'] != NumeroEstacion)):
                    NumberOfBikes+=1
                else:
                    #print("Algo anda mal")
                    #print(i['Origen_Id'])
                    #print(i['Destino_Id'])
                    break
                if((NumberOfBikes < int( (Threshold_Action) * NumberofDocks_Station10 )) |                     (NumberOfBikes > int( (1-Threshold_Action) * NumberofDocks_Station10 ))):
                    #print("Camioncito de relocacion")
                    #print("Dejando la estacion al " + str(cur_RebalPerc) + "%")
                    NumberOfBikes = int((cur_RebalPerc*NumberofDocks_Station10) / 100)
                    OptimizationBadEvents+= 1
                #else:
                    #print("All is gut " + str(NumberOfBikes))

            ResultsOptimization.append([cur_RebalPerc, OptimizationBadEvents])
        #print(ResultsOptimization)

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
        #print("The optimal percentage of bikes to start is: "+ str(Percentage))
        #print("The number of relocations needed were:", MinNumberofBadEvents)

        #OptimizationWeekDay Description:

        #[0]DayinYear corresponds to Monday, Tuesday, Wednesday, etc
        #[1]SameEventPercentages is an array with all the percentages that matched the MinNumberofBadEvents
        #[2]Average is the average of all the elements in SameEventPercentages
        #[3]Percentage is the maximum of SameEvent Percentages
        #[4]MinNumberofBadEvents is the minimum number of bike relocation events for every element of rebalancing
        #    percentages on SameEventPercentages

        OptimizationWeekDay.append([DayinYear,SameEventPercentages,Average,Percentage,MinNumberofBadEvents,DayName])
        
    OptimizationWeek.append(OptimizationWeekDay)


# In[ ]:


for optim_day in OptimizationWeek:
    AveragePerforAllSameDay = 0
    AverageRelocations = 0
    for element in optim_day:
        AveragePerforAllSameDay += element[2]
        AverageRelocations += element[-2]

    if(len(OptimizationWeekDay) != 0):
        AveragePerforAllSameDay /= len(OptimizationWeekDay)
        AverageRelocations /= len(OptimizationWeekDay)

    
    print(optim_day[0][-1] + ': ' + 'AverageRelocYear: ' + str(AverageRelocations))
    print("Relocation Average per event: " + str(AveragePerforAllSameDay))
    print()
    
    


# In[ ]:





# In[ ]:




