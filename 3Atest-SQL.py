#!-*-coding:utf-8-*-
import pymysql
import pexpect
import os
import sys
import re
import threading
import time
import queue

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
	loginIp = []
	conn = pymysql.connect(host='localhost',user='gdnoc',passwd='123456Qw!',db='ipran',port=3306)
	cur = conn.cursor()
	sql = 'select * from AAAcsv'
	cur.execute(sql)
	result = cur.fetchall()
	for row in result:
		loginIp.append(row[1])

	resultDict = {}

	myQueue = queue.Queue()
	for ip in loginIp:
		myQueue.put(ip)

	lock = threading.Lock()
	threads = []
	for i in range(20):
		threads.append(BD_Result_Thread(lock,"thread-" + str(i)))
	for t in threads:
		t.start()
	for t in threads:
		t.join()

except pymysql.Error as e:
	print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

finally:
	for key in resultDict:
	    cur.execute('update AAAcsv set Telnet = "%s",HostName = "%s" where LoginIp = "%s"' % tuple(resultDict[key] + [key]))
	cur.close()
	conn.commit()
	conn.close()