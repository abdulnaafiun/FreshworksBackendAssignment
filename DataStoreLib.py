'''
Program Created by Abdul Naafi Un
'''
import sys
import os.path
from os import path
import json
import time
import threading
class InitDataStore:
	def getdatastorepath(self):
		return self.__filePath
	
	def __init__(self,path='DataStoreFile.dat'):
		self.__lock=None
		self.__filePath=None
		self.__lockFile=None
		if(len(path)>0):
			self.__lock=None
			self.__filePath=path
			self.__lockFile=path+'.lock'				
			f= open(path,"a+")
			f.close()
		else:
			print("Invalid DataStore FileName")
			return None
		try:
			self.__lock=open(self.__lockFile,"x")
			print("Data Store Initialized Successfully : "+self.__filePath +" and locked for Single Client. Multi Threaded Process are still allowed to access.")
		except FileExistsError:
			print("DataStore already in use by another process")
			self.__lock=None
			self.__filePath=None
			self.__lockFile=None
			return


	def __del__(self):
		if self.__lock is not None:
			self.__lock.close()
			os.remove(self.__lockFile)
	

class ManipulateDataSource(threading.Thread):
	__threadLock=threading.Lock()

	def __init__(self,datastore):
		self.__datastore=None
		self.__datastorepath=None
		self.__threadLock=None
		if(datastore.getdatastorepath() is None):
			print("Invalid DataStore to perform Data Manipulation")
			return
		
		threading.Thread.__init__(self)
		self.__datastore=datastore
		self.__datastorepath=datastore.getdatastorepath()
		self.__threadLock=ManipulateDataSource.__threadLock

	def createDataStoreRecord(self,key,value,ttl):
		localPath=self.__datastorepath
		if(localPath is None):
			return ("Invalid DataStore to perform Data Manipulation - Cread/Add")
		threadcount=threading.active_count()
		self.__threadLock.acquire()
		if(threading.active_count()>1):
			print ('Lock acquired by %s' % threading.current_thread())
		
		if(len(key)>32):
			returnstring= "Length of Key ->"+key+" is more than 32 Characters"
			self.__threadLock.release()
			if(threading.active_count()>1):
				print ('Lock released by %s' % threading.current_thread())
			#print(returnstring)
			return returnstring
		if((type(value)!=dict) and (type(value)!=list)):
			self.__threadLock.release()
			if(threading.active_count()>1):
				print ('Lock released by %s' % threading.current_thread())
			return ("Error : Invalid JSON Object")
		localPath=self.__datastorepath
		f= open(localPath,"r")
		contents=f.read()
		f.close()
		try:
			dsFileContents= json.loads(contents)
		except:
			if(len(contents.strip())>0):
				self.__threadLock.release()
				if(threading.active_count()>1):
					print()
				return ("File Illegally Modified  by External Program")
			else:
				dsFileContents={}
			
		if key in dsFileContents:
			self.__threadLock.release()
			if(threading.active_count()>1):
				print ('Lock released by %s' % threading.current_thread())
			returnstring="Error : Key ->"+key+ " already exist."
			return returnstring
		else:
			temp_jsonString=json.dumps(value)
			sizefromprogram=sys.getsizeof(temp_jsonString)
			f= open("temp.dump","w+")
			f.write(temp_jsonString)
			f.close()
			sizefromos=os.path.getsize('temp.dump')
			os.remove('temp.dump')
			sizefromos_ds=os.path.getsize(self.__datastorepath)
			finalsize=sizefromos_ds+sizefromos
			if(finalsize>1073741824):
				returnstring="Error : Size of JSON Object Value for the key ->"+key+ " is exceeding 1 GB File Size"
				return returnstring
			
			if(sizefromos>16384 or sizefromprogram>16384):
				return ("Error : Size of JSON Object Value for the key ->"+key+ " is exceeding 16 KB of memory")
			expiry_datetime=0
			if(ttl>0):
				expiry_datetime=time.time()+ttl
			TTL_Value_Dict={ "ttl":expiry_datetime, "value":value}
			dsFileContents[key]=TTL_Value_Dict			
			f= open(self.__datastorepath,"w+")
			f.write(json.dumps(dsFileContents,indent=4))
			f.close()
		#print ('Lock released by %s' % threading.current_thread())
		self.__threadLock.release()
		if(threading.active_count()>1):
			print ('Lock released by %s' % threading.current_thread())
			
		return ("Key Value Pair Created for key ->"+key)
	def createKeyValuePair(self,key,value,ttl=None):
		if(ttl is None):
			return (self.createDataStoreRecord(key,value,0))
		elif(ttl<1):
			return ("Error : Invalid TTL for the key ->"+key + "")
		else:
			return (self.createDataStoreRecord(key,value,ttl))
			
	def readKeyValuePair(self,key):
		localPath=self.__datastorepath
		if(localPath is None):
			return "Invalid DataStore to perform Data Manipulation - Read"
			
		#print(self.__datastorepath)
		f= open(localPath,"r")
		contents=f.read()
		try:
			dsFileContents= json.loads(contents)
			f.close()
		except:
			if(len(contents.strip())>0):
				#print(len(contents.strip()))
				return "Error : File Illegally Modified Externaly by Other Program"
			else:
				return "DataStore is Empty. DataStore Modified either by external program or, data doesn't exist in it."

		if key in dsFileContents:
			if dsFileContents[key]['ttl']==0:
				return(dsFileContents[key]['value'])
			elif dsFileContents[key]['ttl'] >= time.time():
				return (dsFileContents[key]['value'])
			else:
				return "Note : Key ->"+key + " has expired. Unavailable for Read or Delete"
				
		else:
			return "Error : Key ->"+key + " doesn't exist."
		

	def deleteKeyValuePair(self,key):
		localPath=self.__datastorepath
		if(localPath is None):
			return("Invalid DataStore to perform Data Manipulation - Delete")

		#print(self.__datastorepath)
		f= open(localPath,"r")
		contents=f.read()
		dsFileContents= json.loads(contents)
		if key in dsFileContents:
			if dsFileContents[key]['ttl']==0:
				dsFileContents.pop(key, None)
				f= open(self.__datastorepath,"w+")
				#print(sys.getsizeof((json.dumps(dsFileContents))))
				f.write(json.dumps(dsFileContents))
				f.close()
				return("Key ->" +key+" deleted successfully")
			elif dsFileContents[key]['ttl'] >= time.time():
				dsFileContents.pop(key, None)
				f= open(self.__datastorepath,"w+")
				#print(sys.getsizeof((json.dumps(dsFileContents))))
				f.write(json.dumps(dsFileContents))
				f.close()
				return("Key ->" +key+" deleted successfully")
			else:
				return "Note : Key ->"+key + " has expired. Unavailable for Read or Delete"
		else:
			return "Error : Key ->"+key + " doesn't exist."

