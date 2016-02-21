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

class BS_Fiber_Thread(threading.Thread):
	"""docstring for BS_Fiber_Thread"""
	def __init__(self,lock,threadName):
		super(BS_Fiber_Thread, self).__init__(name = threadName)
		self.lock = lock

	def run(self):
		global myQueue
		global listResult
		global errList
		while True:
			try:
				hostIp = myQueue.get(block = False)
				if hostIp is None:
					break
				if hostIp == '':
					break
				# result,errHost = BS_Fiber(hostIp)
				result = BS_Fiber(hostIp)
				print (self.name, hostIp)
				# self.lock.acquire()
				# errList = errList + errHost
				# self.lock.release()
				self.lock.acquire()
				listResult = listResult + result
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

def BS_Fiber(ip):
	resultList = []
	# errList = []
	try:
		c = connect.Connector('gdcwb','123456Qw!2')
		child, loginMode = c.connectIPRAN(ip)
		if loginMode == 'Local' or loginMode == '3A':
			result_bs = cmd.cmd_show(child,'show vpws-redundancy arp-cache all','More','>')
			totalCount = int(re.search(r'(?<=totalCount is )(\d+)',result_bs).group())
			if totalCount > 0:
				tmp = re.sub(r'[\r+\n+\t+]',' ',result_bs)
				tmpBS = tmp.split('-------------------------------')
				countBS = len(tmpBS)-1
				for i in range(countBS):
					srcip = re.search(r'(?<=src ip )((\d+\.){3}\d+)',tmpBS[i])
					if srcip:
						resultDict = {}
						srcip = srcip.group()
						smac = re.search(r'(?<=smac )(([a-z0-9]+\.){2}[a-z0-9]+)',tmpBS[i]).group()
						resultDict['BS_IP'] = srcip
						resultDict['BS_MAC'] = smac
						resultDict['A_IP'] = ip
						resultList.append(resultDict)
		elif loginMode == 'No' or loginMode == 'Failed':
			print(ip + ' cannot login in')
			# errList.append(ip)
		return resultList
	except Exception as e:
			print(ip + ' error!!')
			print(e)

try:
	loginIp = rw.ReadFromTxt('err.txt')
	myQueue = queue.Queue()
	for ip in loginIp:
		myQueue.put(ip)

	listResult = []
	# errList = []
	lock = threading.Lock()
	threads = []
	for i in range(40):
		threads.append(BS_Fiber_Thread(lock,"thread-" + str(i)))
	for t in threads:
		t.start()
	for t in threads:
		t.join()

except Exception as e:
	print(e)

finally:
	fieldnames = ['BS_IP','BS_MAC','A_IP']
	dt = datetime.now()
	strFileName = str(dt.strftime('%m-%d %H.%M')) + '.csv'
	rw.DictWriteToCsv(strFileName, fieldnames, listResult)
	# for ip in errList:
	# 	print(ip)