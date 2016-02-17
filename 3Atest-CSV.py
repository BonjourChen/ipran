#!-*-coding:utf-8-*-
import pymysql
import pexpect
import os
import sys
import re
import threading
import time
import queue
from datetime import datetime

varPath = os.path.dirname(__file__)
if varPath not in sys.path:
	sys.path.insert(0, varPath)

from IPRANLibs import *

class AAAtest_Thread(threading.Thread):
	"""docstring for AAAtest_Thread"""
	def __init__(self,lock,threadName):
		super(AAAtest_Thread, self).__init__(name = threadName)
		self.lock = lock

	def run(self):
		global myQueue
		global resultDict
		while True:
			try:
				hostIp = myQueue.get(block = False)
				if hostIp is None:
					break
				if hostIp == '':
					break
				listResult = AAAtest(hostIp)
				print (self.name, hostIp)
				self.lock.acquire()
				resultDict[hostIp] = listResult
				self.lock.release()
			except queue.Empty:
				print(self.name + ' finish at %s' %time.ctime())
				break

def getHosename(child):
	loginprompt = '[#>]'
	child.send('\r\n')
	child.expect(loginprompt)
	tmpStr = str(child.before, encoding = 'utf-8')
	if re.search(r'(?<=\<)[a-zA-Z0-9\.-]*',tmpStr):
		hostname = re.search(r'(?<=\<)[a-zA-Z0-9\.-]*',tmpStr).group()
	elif re.search(r'[a-zA-Z0-9\.-]*',tmpStr):
		hostname = re.search(r'(?<=\n)[a-zA-Z0-9\.-]*',tmpStr).group()
	else:
		hostname = str(child.before, encoding = 'utf-8')
	return hostname

def AAAtest(ip):
	listResult = []
	try:
		c = connect.Connector('gdcwb','123456Qw!2')
		child, loginMode = c.connectIPRAN(ip)
		if loginMode == '3A':
			listResult.append('3A')
			hostname = getHosename(child)
			listResult.append(hostname)
		elif loginMode == 'Local':
			listResult.append('Local')
			hostname = getHosename(child)
			listResult.append(hostname)
		elif loginMode == 'Failed':
			listResult = ['Failed','']
		elif loginMode == 'No':
			listResult = ['No','']
		if loginMode == 'Failed' or loginMode == 'No':
			print(ip + ' Login Failed')
		return listResult
	except Exception as e:
			print(e)

try:
	loginIp = rw.ReadFromTxt('err.txt')
	print(loginIp)
	myQueue = queue.Queue()
	for ip in loginIp:
		myQueue.put(ip)

	resultDict = {}
	lock = threading.Lock()
	threads = []
	for i in range(20):
		threads.append(AAAtest_Thread(lock,"thread-" + str(i)))
	for t in threads:
		t.start()
	for t in threads:
		t.join()

except Exception as e:
	print(e)

finally:
	fieldnames = ['LoginIp','Telnet','HostName']
	dt = datetime.now()
	strFileName = str(dt.strftime('%m-%d %H.%M')) + '.csv'
	dictData = [dict(zip(fieldnames, tmp)) for tmp in [[key] + resultDict[key] for key in resultDict]]
	print(dictData)
	rw.DictWriteToCsv(strFileName, fieldnames, dictData)