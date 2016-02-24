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
a = {'4.112.225.96': [{'BS_MAC': 'e4c2.d1eb.8836', 'PW': 'pw10028', 'A_YW_IP': '3.112.225.96', 'B_IP': '4.112.224.57', 'BS_IP': '8.152.13.39'}]}
c = {'4.112.224.59': [{'BS_MAC': 'e4c2.d1e9.804f', 'PW': 'pw10019', 'A_YW_IP': '3.112.224.59', 'B_IP': '4.112.224.57', 'BS_IP': '8.152.13.38'}]}
b = {'4.112.224.59': [{'BS_MAC': 'e4c2.d1eb.883a', 'PW': 'pw10018', 'A_YW_IP': '3.112.224.59', 'B_IP': '4.112.224.57', 'BS_IP': '8.152.13.18'}]}
e = {}
for k,v in a.items():
	if k in b.keys():
		b[k] += v
	else:
		b[k] = v

for k,v in b.items():
	t = {}
	t[k] = v
	print(t)
	

# l = []
# for k,v in b.items():
# 	for i in v:
# 		m = {} 
# 		m['A_WG_IP'] = k
# 		m['BS_IP'] = i['BS_IP']
# 		m['BS_MAC'] = i['BS_MAC']
# 		m['A_YW_IP'] = i['A_YW_IP']
# 		m['PW'] = i['PW']
# 		m['B_IP'] = i['B_IP']
# 		l.append(m)

# fieldnames = ['BS_IP','BS_MAC','A_WG_IP','A_YW_IP','PW','B_IP']
# dt = datetime.now()
# strFileName = str(dt.strftime('%m-%d %H.%M')) + '.csv'
# rw.DictWriteToCsv(strFileName, fieldnames, l)