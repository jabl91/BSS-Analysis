#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""This module serves as an interface with Pyota,
"""

from iota import Iota
from iota import TryteString
from iota import Address, ProposedTransaction, Tag, Transaction
from iota import Bundle
from iota import Address, ProposedBundle, ProposedTransaction
from iota.crypto.signing import KeyGenerator

import datetime
import time
import re


class IOTAInterface:

    def __init__(self):
        
        self.api = Iota('https://potato.iotasalad.org:14265','SMRUKAKOPAKXQSIKVZWQGQNKZZWL9BGEFJCIEBRJDIAGWFHUKAOSWACNC9JFDU9WHAPZBEIGWBU9VTNZS')

        #print(self.api.get_node_info())
		
		
    def getAllBatteriesData(self):

        Batteries = {}

        for iterator in range(0,9):

            MyBatteryTimeStamp = time.localtime().tm_year*1000
            MyBatteryTimeStamp += time.localtime().tm_yday
            print(MyBatteryTimeStamp)

            TagToFind = TryteString.from_string(str(MyBatteryTimeStamp))
            TagToFind = str(TagToFind) + chr(ord('A') + iterator)
            print(TagToFind)

            myResults = self.api.find_transactions(tags = [str(TagToFind)])

            print(myResults)

            # In[4]:


            max = 0.0
            id = 0

            for idx, result in enumerate(myResults['hashes']):

                #TestBundle = self.api.get_bundles(myResults['hashes'][0])
                TestBundle = self.api.get_bundles(result)

                currentTimestamp = TestBundle['bundles'][0].transactions[0].attachment_timestamp*0.001

                print(currentTimestamp)

                if currentTimestamp > max:
                    max = currentTimestamp
                    id = idx
                    message = TestBundle['bundles'][0].transactions[0].signature_message_fragment


			# In[5]:



            if max != 0.0:
                print(max,id)
                print(datetime.datetime.fromtimestamp(max).strftime('%c'))
                print(TryteString.as_string(message))

                prog = re.compile("\D+(\d+)%\D+(\d+)\D+is (\w+)\n\D+(\d+)")
                result = prog.match(TryteString.as_string(message))

                print(result.group(1))
                print(result.group(2))
                print(result.group(3))
                print(result.group(4))

                CurrentBattery = {"BatteryId":int(result.group(4))}
                CurrentBattery.update({"Voltage" : int(result.group(2))})
                CurrentBattery.update({"ChargingState" : str(result.group(3))})
                CurrentBattery.update({"BatteryLevel" : int(result.group(1))})
                CurrentBattery.update({"TimeStamp" : str(datetime.datetime.fromtimestamp(max).strftime('%c'))})

                Batteries.update({str(CurrentBattery["BatteryId"]):CurrentBattery})
                print(Batteries)
				
        return Batteries


				
				
				
				
				
if __name__ == "__main__":

    myMonitor = IOTAInterface()

    myMonitor.getAllBatteriesData()
				
				
				
# if __name__ == "__main__":

	# Batteries = {}

	# for iterator in range(0,9):

		# MyBatteryTimeStamp = time.localtime().tm_year*1000
		# MyBatteryTimeStamp += time.localtime().tm_yday
		# print(MyBatteryTimeStamp)

		# TagToFind = TryteString.from_string(str(MyBatteryTimeStamp))
		# TagToFind = str(TagToFind) + chr(ord('A') + iterator)
		# print(TagToFind)

		# myMonitor = IOTAInterface()
		# myResults = myMonitor.api.find_transactions(tags = [str(TagToFind)])

		# print(myResults)

		# # In[4]:


		# max = 0.0
		# id = 0

		# for idx, result in enumerate(myResults['hashes']):

			# #TestBundle = myMonitor.api.get_bundles(myResults['hashes'][0])
			# TestBundle = myMonitor.api.get_bundles(result)

			# currentTimestamp = TestBundle['bundles'][0].transactions[0].attachment_timestamp*0.001

			# print(currentTimestamp)

			# if currentTimestamp > max:
				# max = currentTimestamp
				# id = idx
				# message = TestBundle['bundles'][0].transactions[0].signature_message_fragment


		# # In[5]:



		# if max != 0.0:
			# print(max,id)
			# print(datetime.datetime.fromtimestamp(max).strftime('%c'))
			# print(TryteString.as_string(message))
			
			# prog = re.compile("\D+(\d+)%\D+(\d+)\D+is (\w+)\n\D+(\d+)")
			# result = prog.match(TryteString.as_string(message))
			
			# print(result.group(1))
			# print(result.group(2))
			# print(result.group(3))
			# print(result.group(4))
			
			# CurrentBattery = {"BatteryId":int(result.group(4))}
			# CurrentBattery.update({"Voltage" : int(result.group(2))})
			# CurrentBattery.update({"ChargingState" : str(result.group(3))})
			# CurrentBattery.update({"BatteryLevel" : int(result.group(1))})
			
			# Batteries.update({str(CurrentBattery["BatteryId"]):CurrentBattery})
			# print(Batteries)

