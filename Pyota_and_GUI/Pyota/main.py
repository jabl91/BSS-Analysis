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


class IOTAInterface:

    def __init__(self):
        
        self.api = Iota('https://potato.iotasalad.org:14265','SMRUKAKOPAKXQSIKVZWQGQNKZZWL9BGEFJCIEBRJDIAGWFHUKAOSWACNC9JFDU9WHAPZBEIGWBU9VTNZS')

        #print(self.api.get_node_info())

    
    
if __name__ == "__main__":
    
    myMonitor = IOTAInterface()
    myResults = myMonitor.api.find_transactions(tags = ['BATC99999999999999999999999'])
    
    print(myResults)
    
    max = 0.0
    id = 0
    
    for idx, result in enumerate(myResults['hashes']):
        
        #TestBundle = myMonitor.api.get_bundles(myResults['hashes'][0])
        TestBundle = myMonitor.api.get_bundles(result)
    
        currentTimestamp = TestBundle['bundles'][0].transactions[0].attachment_timestamp*0.001
        
        print(currentTimestamp)
        
        if currentTimestamp > max:
            max = currentTimestamp
            id = idx
            message = TestBundle['bundles'][0].transactions[0].signature_message_fragment
    
    print(max,idx)
    print(datetime.datetime.fromtimestamp(max).strftime('%c'))
    print(TryteString.as_string(message))
	
	