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


class BS_Fiber_Ainfo_Thread(threading.Thread):
	"""docstring for BS_Fiber_Ainfo_Thread"""
	def __init__(self,lock,threadName):
		super(BS_Fiber_Ainfo_Thread, self).__init__(name = threadName)
		self.lock = lock

	def run(self):
		global BsQueue
		global listResultFinal
		while True:
			try:
				info = BsQueue.get(block = False)
				result = BS_Fiber_Ainfo(info)
				print (self.name, info)
				self.lock.acquire()
				listResultFinal.append(result)
				self.lock.release()
			except queue.Empty:
				print(self.name + ' finish at %s' %time.ctime())
				break


def BS_Fiber(ip):
	try:
		listBSInfo =[]
		c = connect.Connector('gdcwb','123456Qw!2')
		child,loginMode = c.connectIPRAN(ip)
		if loginMode == 'Local' or loginMode == '3A':
			result_cdma_ran = cmd.cmd_show(child, 'show arp all include CDMA-RAN', 'More', '#')
			cdma_ran_Line = re.findall(r'(virtual.*)/\-',result_cdma_ran)
			countBS = len(cdma_ran_Line)
			if countBS == 0:
				print(ip + ' has no basic station.')
			else:
				for line in range(countBS):
					gatewayBS = re.search(r'Interface',cdma_ran_Line[line])
					if gatewayBS:
						pass
					else:
						info = {}
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
						while True:
							pw = re.search(r'(?<!description )pw\d+',result_interface_conf)
							aip = re.search(r'(\d+\.){3}\d+',result_interface_conf)
							if pw and aip:
								pw = pw.group()
								aip = aip.group()
								break
						info['BS_IP'] = BS_IP
						info['BS_MAC'] = BS_MAC
						info['A_YW_IP'] = aip
						info['PW'] = pw
						info['B_IP'] = ip
						print(info)
						listBSInfo.append(info)
			child.close(force=True)
		else:
			print(ip + ' can\'t login.')
			rw.WriteToTxt('errIP.txt',ip+'\r')
			child.close()
		return listBSInfo
	except Exception as e:
		print(ip + ' ERROR!!')
		print(e)


def BS_Fiber_Ainfo_bak(info):
	try:
		c = connect.Connector('gdcwb','123456Qw!2')
		child, loginMode = c.connectIPRAN(info['B_IP'])
		child, loginMode = cmd.cmd_telnet(child,info['A_YW_IP'])
		if loginMode == 'Local' or loginMode == '3A':
			child.send('en' + '\r')
			result_loopback_A = cmd.cmd_show(child,'show running-config interface loopback1023','More','#')
			result_interface = cmd.cmd_show(child,'show mpls l2-circuit '+ info['PW'] +'\r','More','#')
			while True:
				result_loopback_A = re.search(r'(\d+\.){3}\d+',result_loopback_A)
				result_interface = re.search(r'GE\d+/\d+/\d+\.\d+',result_interface)
				if result_loopback_A and result_interface:
					result_loopback_A = result_loopback_A.group()
					result_interface = result_interface.group()
					info['A_WG_IP'] = result_loopback_A
					info['A_PORT'] = result_interface
					break
		else:
			print(info['A_YW_IP'] + ' can\'t login.')
			info['A_WG_IP'] = re.sub(r'3([\.\d+]{3})', r'4\1', info['A_YW_IP'])
			child, loginMode = c.connectIPRAN(info['A_WG_IP'])
			if loginMode == '3A' or loginMode == 'Local':
				child.send('en' + '\r')
				result_loopback_A = cmd.cmd_show(child,'show running-config interface loopback1023','More','#')
				result_interface = cmd.cmd_show(child,'show mpls l2-circuit '+ info['PW'] +'\r','More','#')
				while True:
					result_loopback_A = re.search(r'(\d+\.){3}\d+',result_loopback_A)
					result_interface = re.search(r'GE\d+/\d+/\d+\.\d+',result_interface)
					if result_loopback_A and result_interface:
						result_loopback_A = result_loopback_A.group()
						result_interface = result_interface.group()
						info['A_PORT'] = result_interface
						break
			else:
				print(info['A_WG_IP'] + ' can\'t login.')
				info['A_PORT'] = ''
		child.close(force=True)
		return info
	except Exception as e:
		print(info['A_YW_IP'] + ' ERROR!!')
		print(e)


def BS_Fiber_Ainfo(info):
	try:
		c = connect.Connector('gdcwb','123456Qw!2')
		info['A_WG_IP'] = re.sub(r'3([\.\d+]{3})', r'4\1', info['A_YW_IP'])
		child, loginMode = c.connectIPRAN(info['A_WG_IP'])
		if loginMode == '3A' or loginMode == 'Local':
			child.send('en' + '\r')
			result_loopback_A = cmd.cmd_show(child,'show running-config interface loopback1023','More','#')
			result_interface = cmd.cmd_show(child,'show mpls l2-circuit '+ info['PW'] +'\r','More','#')
			while True:
				result_loopback_A = re.search(r'(\d+\.){3}\d+',result_loopback_A)
				result_interface = re.search(r'GE\d+/\d+/\d+\.\d+',result_interface)
				if result_loopback_A and result_interface:
					result_loopback_A = result_loopback_A.group()
					result_interface = result_interface.group()
					info['A_PORT'] = result_interface
					break
		else:
			print(info['A_WG_IP'] + ' can\'t login.')
			info['A_PORT'] = ''
		child.close(force=True)
	except Exception as e:
		info['A_PORT'] = ''
		print(info['A_WG_IP'] + ' ERROR!!')
		print(e)
	finally:
		return info

try:
	loginIp = rw.ReadFromTxt('host.txt')
	myQueue = queue.Queue()
	for ip in loginIp:
		myQueue.put(ip)

	listResult = []
	lock = threading.Lock()
	threads = []
	for i in range(3):
		threads.append(BS_Fiber_Thread(lock,"thread-" + str(i)))
	for t in threads:
		t.start()
	for t in threads:
		t.join()

	BsQueue = queue.Queue()
	for d in listResult:
		BsQueue.put(d)

	listResultFinal = []
	lock = threading.Lock()
	threads = []
	for i in range(3):
		threads.append(BS_Fiber_Ainfo_Thread(lock,"thread-" + str(i)))
	for t in threads:
		t.start()
	for t in threads:
		t.join()

except Exception as e:
	print(e)

finally:
	fieldnames = ['BS_IP','BS_MAC','A_WG_IP','A_YW_IP','A_PORT','PW','B_IP']
	dt = datetime.now()
	strFileName = str(dt.strftime('%m-%d %H.%M')) + '.csv'
	rw.DictWriteToCsv(strFileName, fieldnames, listResultFinal)
