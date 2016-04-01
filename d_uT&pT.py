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

class BD_Result_Thread(threading.Thread):
	"""docstring for BD_Result_Thread"""
	def __init__(self,lock,threadName):
		super(BD_Result_Thread, self).__init__(name = threadName)
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
				listResult = bd_result(hostIp)
				print (self.name, hostIp)
				self.lock.acquire()
				resultDict[hostIp] = listResult
				#print(listResult)
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

def HW_B(child, listResult):
	result_isis = cmd.cmd_show(child,'dis isis peer','More','>')
	listBPeer = re.findall(r'[a-zA-Z0-9\.-]+-B-[a-zA-Z0-9\.-]*(?=\s+)', result_isis)
	listDPeer = re.findall(r'[a-zA-Z0-9\.-]+-D-[a-zA-Z0-9\.-]*(?=\s+)', result_isis)
	listMPeer = re.findall(r'[a-zA-Z0-9\.-]+-M-[a-zA-Z0-9\.-]*(?=\s+)', result_isis)
	listXPeer = re.findall(r'[a-zA-Z0-9\.-]+-X-[a-zA-Z0-9\.-]*(?=\s+)', result_isis)
	nBPeer = len(set(listBPeer))
	nDPeer = len(set(listDPeer))
	nMPeer = len(set(listMPeer))
	nXPeer = len(set(listXPeer))
	listResult.append(str(nBPeer))
	listResult.append(str(nDPeer))
	listResult.append(str(nMPeer))
	listResult.append(str(nXPeer))

	if '-D-' in listResult[1]:
		if nMPeer >= 1 and nDPeer >= 1:
			listResult.append('OK')
		elif nXPeer >= 1 and nDPeer >= 1:
			listResult.append('OK')
		elif (nMPeer >= 1 and nDPeer < 1) or (nXPeer >= 1 and nDPeer < 1):
			listResult.append('Only uT')
		elif (nDPeer >= 1 and nMPeer < 1) or (nDPeer >= 1 and nXPeer < 1):
			listResult.append('Only pT')
		else:
			listResult.append('unknown')
	else:
		listResult.append('unknown')
	return listResult
	
def ZTE_B(child, listResult):
	result_isis = cmd.cmd_show(child,'show isis adjacency','More','#')
	listBPeer = re.findall(r'[a-zA-Z0-9\.-]+-B-[a-zA-Z0-9\.-]*(?=\s+)', result_isis)
	listDPeer = re.findall(r'[a-zA-Z0-9\.-]+-D-[a-zA-Z0-9\.-]*(?=\s+)', result_isis)
	listMPeer = re.findall(r'[a-zA-Z0-9\.-]+-M-[a-zA-Z0-9\.-]*(?=\s+)', result_isis)
	listXPeer = re.findall(r'[a-zA-Z0-9\.-]+-X-[a-zA-Z0-9\.-]*(?=\s+)', result_isis)
	nBPeer = len(set(listBPeer))
	nDPeer = len(set(listDPeer))
	nMPeer = len(set(listMPeer))
	nXPeer = len(set(listXPeer))
	listResult.append(str(nBPeer))
	listResult.append(str(nDPeer))
	listResult.append(str(nMPeer))
	listResult.append(str(nXPeer))

	if '-D-' in listResult[1]:
		if nMPeer >= 1 and nDPeer >= 1:
			listResult.append('OK')
		elif nXPeer >= 1 and nDPeer >= 1:
			listResult.append('OK')
		elif (nMPeer >= 1 and nDPeer < 1) or (nXPeer >= 1 and nDPeer < 1):
			listResult.append('Only uT')
		elif (nDPeer >= 1 and nMPeer < 1) or (nDPeer >= 1 and nXPeer < 1):
			listResult.append('Only pT')
		else:
			listResult.append('unknown')
	else:
		listResult.append('unknown')
	return listResult

def Fiber_B(child, listResult):
	result_isis = cmd.cmd_show(child,'show clns is-neighbors','More','#')
	listBPeer = re.findall(r'[a-zA-Z0-9\.-]+-B-[a-zA-Z0-9\.-]*(?=\s+)', result_isis)
	listDPeer = re.findall(r'[a-zA-Z0-9\.-]+-D-[a-zA-Z0-9\.-]*(?=\s+)', result_isis)
	listMPeer = re.findall(r'[a-zA-Z0-9\.-]+-M-[a-zA-Z0-9\.-]*(?=\s+)', result_isis)
	listXPeer = re.findall(r'[a-zA-Z0-9\.-]+-X-[a-zA-Z0-9\.-]*(?=\s+)', result_isis)
	nBPeer = len(set(listBPeer))
	nDPeer = len(set(listDPeer))
	nMPeer = len(set(listMPeer))
	nXPeer = len(set(listXPeer))
	listResult.append(str(nBPeer))
	listResult.append(str(nDPeer))
	listResult.append(str(nMPeer))
	listResult.append(str(nXPeer))

	if '-D-' in listResult[1]:
		if nMPeer >= 1 and nDPeer >= 1:
			listResult.append('OK')
		elif nXPeer >= 1 and nDPeer >= 1:
			listResult.append('OK')
		elif (nMPeer >= 1 and nDPeer < 1) or (nXPeer >= 1 and nDPeer < 1):
			listResult.append('Only uT')
		elif (nDPeer >= 1 and nMPeer < 1) or (nDPeer >= 1 and nXPeer < 1):
			listResult.append('Only pT')
		else:
			listResult.append('unknown')
	else:
		listResult.append('unknown')
	return listResult

def bd_result(ip):
	listResult = []
	try:
		c = connect.Connector('gdcwb','123456Qw!2')
		child, loginMode = c.connectIPRAN(ip)
		if loginMode == '3A':
			listResult.append('3A')
		elif loginMode == 'Local':
			listResult.append('Local')
		elif loginMode == 'Failed':
			listResult = ['Failed','','','','','','','']
		elif loginMode == 'No':
			listResult = ['No','','','','','','','']

		if loginMode == '3A' or loginMode == 'Local':
			hostname = getHosename(child)
			listResult.append(hostname)
			#print(hostname)
			if re.search(r'910|950',hostname):
				listResult.append('HW-A')
			elif re.search(r'CX600',hostname):
				listResult.append('HW-B/D')
				listResult = HW_B(child, listResult)
			elif re.search(r'6130|6150|6220',hostname):
				listResult.append('ZTE-A')
			elif re.search(r'9000',hostname):
				listResult.append('ZTE-B/D')
				listResult = ZTE_B(child, listResult)
			elif re.search(r'R835E|R820',hostname):
				listResult.append('Fiber-A')
			elif re.search(r'R8000',hostname):
				listResult.append('Fiber-B/D')
				listResult = Fiber_B(child,listResult)
			else:
				listResult = [loginMode,'Unknown','','','','','','']
			child.close()
		elif loginMode == 'Failed' or loginMode == 'No':
			print(ip + ' Login Failed')
		return listResult
	except Exception as e:
			print(e)

try:
	loginIp = []
	conn = pymysql.connect(host='localhost',user='gdnoc',passwd='123456Qw!',db='ipran',port=3306)
	cur = conn.cursor()
	sql = 'select * from bdcsv'
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
	for i in range(10):
		threads.append(BD_Result_Thread(lock,"thread-" + str(i)))
	for t in threads:
		t.start()
	for t in threads:
		t.join()

except pymysql.Error as e:
	print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

finally:
	for key in resultDict:
		cur.execute('''update bdcsv set Telnet = "%s",HostName = "%s", DeviceType = "%s", nBPeer = "%s", nDPeer = "%s", 
			nMPeer = "%s", nXPeer = "%s", Error = "%s" where LoginIp = "%s"''' % tuple(resultDict[key] + [key]))
	cur.close()
	conn.commit()
	conn.close()
