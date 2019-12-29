'''
Program Created by Abdul Naafi Un
'''

from DataStoreLib import InitDataStore
from DataStoreLib import ManipulateDataSource
import json
import sys
import time
import threading
import os
import queue

def SecondClientProcess():
	print()
	print("================================================")
	print("From Cli 2 :  Freshworks – Backend Assignment")
	print("================================================")
	print("From Cli 2:   This client program will try to open the existing DatatStore that has been already opened.")
	
	
	print("From Cli 2 :  Create new DataStore without passing FilePath. This is already opened by previous Client")
	print()
	dataStore=InitDataStore()
	manipulate=ManipulateDataSource(dataStore)
	print()
	
	key="1"
	jsonObject={"id":"0001"}
	ttl=120
	print("From Cli 2 :  Creating Key = "+key+" TTL = "+str(ttl))
	output=manipulate.createKeyValuePair(key,jsonObject,ttl)
	print("From Lib   :  "+output)
	print()
	
	key="1"
	print("From Cli 2 :  Reading Key = "+key)
	output=json.dumps(manipulate.readKeyValuePair(key))
	print("From Lib   :  "+output)
	print()
		
	key="1"
	print("From Cli 2 :  Deleting Key = "+key)
	output=manipulate.deleteKeyValuePair(key)
	print("From Lib   :  "+output)
	print()
	
	print("=====================================")
	print("From Cli 2 :  End of Program Execution")
	print("=====================================")