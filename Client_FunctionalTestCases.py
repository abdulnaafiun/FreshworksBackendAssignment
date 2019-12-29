'''
Program Created by Abdul Naafi Un
'''
import unittest
from DataStoreLib import InitDataStore
from DataStoreLib import ManipulateDataSource
import json
import sys
import time
import threading
import os
def testcases():
	print()
	print("================================================")
	print("From Cli :  Freshworks – Backend Assignment")
	print("================================================")
	print()
	print("From Cli :  Since this is unit test library with all test executions sequenced one by one, the program will \
delete the datastore and a new datastore will be created everytime you run the testscript.")
	if(os.path.exists("NewDataStore.dat")):
		os.remove("NewDataStore.dat")
	if(os.path.exists("NewDataStore.lock")):
		os.remove("NewDataStore.lock")
	print("===================================================")
	print("Test Cases Covered")
	print("===================================================")
	print("1. DataStore Creation with Valid FilePath")
	print("2. DataStore Creation with In-Valid FilePath")
	print("3. Create record with Key Size more than 32 Chars")
	print("4. Create record with Key Size less than 32 Chars")
	print("5. Create record with existing key")
	print("6. Create record with Invalid JSON")
	print("7. Create record with without TTL")
	print("8. Create record with Invalid TTL")
	print("8. Read Valid Record")
	print("9 Read In-Valid Record")
	print("10. Read record with expired TTL")
	print("11. Delete Valid Record")
	print("12. Delete In-Valid Record")
	print("13. Delete record with expired TTL")
	print("14. Additional Error Messages")
	
	print("From Cli :  Trying to Create Blank DataStore Name")
	dataStore=InitDataStore('')
	print()
	
	print("From Cli :  Create New DataStore - NewDataStore.dat")
	dataStore=InitDataStore('NewDataStore.dat')
	manipulate=ManipulateDataSource(dataStore)
	
	print()
	print()

	key="1"
	jsonObject={"id":"0001"}
	ttl=120
	print("From Cli :  Creating Key = "+key+" TTL = "+str(ttl))
	output=manipulate.createKeyValuePair(key,jsonObject,ttl)
	print("From Lib :  "+output)
	print()
	
	key="1"
	print("From Cli :  Reading Key = "+key)
	output=json.dumps(manipulate.readKeyValuePair(key))
	print("From Lib :  "+output)
	print()
	
	key="2"
	jsonObject={"id":"0002"}
	ttl=120
	print("From Cli :  Creating Key = "+key+" TTL = "+str(ttl))
	output=manipulate.createKeyValuePair(key,jsonObject,ttl)
	print("From Lib :  "+output)
	print()
	
	key="2"
	print("From Cli :  Reading Key = "+key)
	output=json.dumps(manipulate.readKeyValuePair(key))
	print("From Lib :  "+output)
	print()
	
	key="3"
	jsonObject={"id":"0001"}
	ttl=3
	print("From Cli :  Creating Key = "+key+" TTL = "+str(ttl))
	output=manipulate.createKeyValuePair(key,jsonObject,ttl)
	print("From Lib :  "+output)
	print()
	
	key="3"
	print("From Cli :  Reading Key Immediately")
	print("From Cli :  Reading Key = "+key)
	output=json.dumps(manipulate.readKeyValuePair(key))
	print("From Lib :  "+output)
	print()
	
	print("From Cli :  Reading Key after 3 Seconds; after TTL expires")
	time.sleep(3)
	key="3"
	print("From Cli :  Reading Key = "+key)
	output=manipulate.readKeyValuePair(key)
	print("From Lib :  "+output)
	print()
	

	key="1"
	jsonObject={}
	ttl=3
	print("From Cli :  Trying to create Key = "+key+" TTL = "+str(ttl)+" which already exist")
	output=manipulate.createKeyValuePair(key,jsonObject,ttl)
	print("From Lib :  "+output)
	print()
	
	
	
	key="abcdefghijklmnopqrstuvwxyzabcdefg"
	print("From Cli :  Trying to create Key = "+key+" TTL = "+str(ttl)+" with Key Length more than 32 chars")
	jsonObject={}
	ttl=120
	output=manipulate.createKeyValuePair(key,jsonObject,ttl)
	print("From Lib :  "+output)
	print()
	
	key="3"
	print("From Cli :  Deleting Key = "+key)
	output=manipulate.deleteKeyValuePair(key)
	print("From Lib :  "+output)
	print()
	
	
	key="3"
	print("From Cli :  Trying to read a key that has been deleted")
	print("From Cli :  Reading Key = "+key)
	output=manipulate.readKeyValuePair(key)
	print("From Lib :  "+output)
	print()
	
	
	
	key="3"
	jsonObject="test"
	ttl=120
	print("From Cli :  Creating Key = "+key+" TTL = "+str(ttl) +" and with invalid JSON Value")
	output=manipulate.createKeyValuePair(key,jsonObject,ttl)
	print("From Lib :  "+output)
	print()

	key="3"
	jsonObject={}
	ttl=0
	print("From Cli :  Creating Key = "+key+" TTL = "+str(ttl) +" and with invalid TTL Value")
	output=manipulate.createKeyValuePair(key,jsonObject,ttl)
	print("From Lib :  "+output)
	print()
	
	key="5"
	jsonObject={}
	ttl=0
	print("From Cli :  Creating Key = "+key+" TTL = "+str(ttl) +" and without TTL Value as this is Optional Field")
	output=manipulate.createKeyValuePair(key,jsonObject)
	print("From Lib :  "+output)
	print()
	
	key="5"
	print("From Cli :  Reading Key = "+key)
	output=json.dumps(manipulate.readKeyValuePair(key))
	print("From Lib :  "+output)
	print()

	key="4"
	print("Trying to Delete Key = "+key +" which doesn't exist")
	print("From Cli :  Deleting Key = "+key)
	output=manipulate.deleteKeyValuePair(key)
	print("From Lib :  "+output)
	print()
	
	key="4"
	jsonObject={"id":"0001"}
	ttl=3
	print("From Cli :  Creating Key = "+key+" TTL = "+str(ttl))
	output=manipulate.createKeyValuePair(key,jsonObject,ttl)
	print("From Lib :  "+output)
	print()
	
	key="4"
	print("From Cli :  Trying to Delete Key = "+key +" with expired TTL")
	print("From Cli :  Deleting Key after 3 Seconds; after TTL expires")
	time.sleep(3)
	print("From Cli :  Deleting Key = "+key)
	output=manipulate.deleteKeyValuePair(key)
	print("From Lib :  "+output)
	print()
	
	print()
	
	print("=====================================")
	print("From Cli :  End of Program Execution")
	print("=====================================")
	print("----------------------------------------------------------------------------------------")

	
if __name__ == '__main__':
    testcases()
