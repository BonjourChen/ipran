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
				result = BS_Fiber(hostIp)
				print (self.name, hostIp)
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
	try:
		listBSInfo =[]
		c = connect.Connector('gdcwb','123456Qw!2')
		child,loginMode = c.connectIPRAN(ip)
		if loginMode == 'Local' or loginMode == '3A':
			result_cdma_ran = cmd.cmd_show(child, 'show arp all include CDMA-RAN', 'More', '#')
			cdma_ran_Line = re.findall(r'(virtual.*)/\-',result_cdma_ran)
			countBS = len(cdma_ran_Line)
			if countBS > 1:
				info = {}
				for line in range(1,countBS)
				lineStr = cdma_ran_Line[line]
				lineStr = re.sub(r'[\s]+',' ',lineStr)
				BS_info = lineStr.split(' ')
				virtualPort = BS_info[0]
				BS_IP = BS_info[1]
				BS_MAC = BS_info[2]
				BS_VLAN = BS_info[6]
				tmp = virtualPort.split('.')
				tmp1 = tmp[0].split('/')
				L2Port = tmp1[0] + '/' + tmp1[1] + '/' + tmp1[2] + '/' + str(int(tmp1[3])-1) +'.' + BS_VLAN
				L2Port = re.sub(r'(^[^0-9]+)',r'\1 ',L2Port)
				result_interface_conf = cmd.cmd_show(child,'show running-config interface '+L2Port,'More','#')
				pw = re.search(r'(?<!description )pw\d+',result_interface_conf).group()
				aip = re.search(r'(\d+\.){3}\d+',result_interface_conf).group()

				info['BS_IP'] = BS_IP
				info['BS_MAC'] = BS_MAC
				info['A_YW_IP'] = aip
				info['PW'] = pw
				info['B_IP'] = ip
			else:
				pass
	except Exception as e:
		print(ip + ' ERROR!!')
		print(e)
	finally:
		fieldnames = ['BS_IP','BS_MAC','A_WG_IP','A_YW_IP','A_PORT','PW','B_IP']