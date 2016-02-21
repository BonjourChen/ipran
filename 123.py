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
resultList = []
g = []
ip = '4.112.224.59'
c = connect.Connector('gdcwb','123456Qw!2')
child, loginMode = c.connectIPRAN(ip)
result_isis = cmd.cmd_show(child,'show vpws-redundancy arp-cache all','More','>')
b = int(re.search(r'(?<=totalCount is )(\d+)',result_isis).group())
if b >0:
	t = re.sub(r'[\r+\n+\t+]',' ',result_isis)
	q = t.split('-------------------------------')
	l = len(q)
	for i in range(l-1):
		print(i)
		s = re.search(r'(?<=src ip )((\d+\.){3}\d+)',q[i])
		if s:
			resultDict = {}
			s = s.group()
			a = re.search(r'(?<=smac )(([a-z0-9]+\.){2}[a-z0-9]+)',q[i]).group()
			resultDict['BS_IP'] = s
			resultDict['BS_MAC'] = a
			# print(s)
			# print(a)
			# print(resultDict)
			resultList.append(resultDict)
			#print(resultList)
g = g + resultList
print(g)
