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
ip = '14.152.242.3'
c = connect.Connector('gdcwb','123456Qw!2')
child, loginMode = c.connectIPRAN(ip)
result_cdma_ran =  cmd.cmd_show(child,'show arp all include CDMA-RAN','More','#')
#print(result_cdma_ran)
a = re.findall(r'(virtual.*)/\-',result_cdma_ran)
#print(a[0])
#print(a[1])
b = a[1]
b = re.sub(r'[\s]+',' ',b)
d = b.split(' ')
e = d[0]
BS_IP = d[1]
BS_MAC = d[2]
BS_VLAN = d[6]
f = e.split('.')
g = f[0].split('/')
L2Port = g[0]+ '/'+g[1]+'/'+g[2]+'/'+ str(int(g[3])-1)+'.'+BS_VLAN
L2Port = re.sub(r'(^[^0-9]+)',r'\1 ',L2Port)
tmp_L2Port = L2Port.split(' ')
L2Port_str = tmp_L2Port[0]
L2Port_num = tmp_L2Port[1]
result_interface_conf = cmd.cmd_show(child,'show running-config interface '+L2Port,'More','#')
pw = re.search(r'(?<!description )pw\d+',result_interface_conf).group()
aip = re.search(r'(\d+\.){3}\d+',result_interface_conf).group()
#print(result_interface_conf)
#print('telnet '+aip)
child_sub,loginMode_sub = cmd.cmd_telnet(child,aip)
child.send('en'+'\r')
result_loopback_A = cmd.cmd_show(child_sub,'show running-config interface loopback1023','More','#')
result_loopback_A = re.search(r'(\d+\.){3}\d+',result_loopback_A).group()
#print(result_loopback_A)
result_interface = cmd.cmd_show(child_sub,'show mpls l2-circuit '+pw+'\r','More','#')
result_interface = re.search(r'GE\d+/\d+/\d+\.\d+',result_interface).group()
print(result_interface)
child_sub.send('exit'+'\r')
tmp1 = cmd.cmd_show(child_sub,'show arp all include CDMA-RAN','More','#')
print(tmp1)
#print(loginMode_sub)
#print(telnet_a)


# result_isis = cmd.cmd_show(child,'show vpws-redundancy arp-cache all','More','>')
# #print(result_isis)
# #print(re.findall(r'.*',result_isis))
# b = int(re.search(r'(?<=totalCount is )(\d+)',result_isis).group())
# if b >0:
# 	t = re.sub(r'[\r+\n+\t+]',' ',result_isis)
# 	q = t.split('-------------------------------')
# 	l = len(q)
# 	for i in range(l-1):
# 		#print(i)
# 		s = re.search(r'(?<=src ip )((\d+\.){3}\d+)',q[i])
# 		if s:
# 			resultDict = {}
# 			s = s.group()
# 			a = re.search(r'(?<=smac )(([a-z0-9]+\.){2}[a-z0-9]+)',q[i]).group()
# 			b = re.search(r'(?<= Arp cache in )(GE\d+/\d+/\d+\.\d+)',q[i]).group()
# 			print(b)
# 			resultDict['A_PORT'] = b
# 			resultDict['BS_IP'] = s
# 			resultDict['BS_MAC'] = a
# 			# print(s)
# 			# print(a)
# 			# print(resultDict)
# 			resultList.append(resultDict)
# 			#print(resultList)
# g = g + resultList
# print(g)
