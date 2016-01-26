#!-*-coding:utf-8-*-
import pymysql
import pexpect
import os
import sys
import re

varPath = os.path.dirname(__file__)
if varPath not in sys.path:
	sys.path.insert(0, varPath)

from IPRANLibs import *


reload(sys)
sys.setdefaultencoding('utf8')

def getHosename(child):
	loginprompt = '[#>]'
	child.send('\r\n')
	child.expect(loginprompt)
	tmpStr = child.before
	if re.search(r'(?<=\<)[a-zA-Z0-9\.-]*',tmpStr):
		hostname = re.search(r'(?<=\<)[a-zA-Z0-9\.-]*',tmpStr).group()
	elif re.search(r'[a-zA-Z0-9\.-]*',tmpStr):
		hostname = re.search(r'(?<=\n)[a-zA-Z0-9\.-]*',tmpStr).group()
	else:
		hostname = child.before
	return hostname


def HW_B(child):
	loginprompt = '[#>]'
	child.sendline('dis isis peer')
	child.expect('dis isis peer')
	child.sendline(' ')
	child.expect(loginprompt)
	result_isis = child.before

	global listResult
	listBPeer = re.findall(r'[a-zA-Z0-9\.-]+-B-[a-zA-Z0-9\.-]*(?=\s+)', result_isis)
	listDPeer = re.findall(r'[a-zA-Z0-9\.-]+-D-[a-zA-Z0-9\.-]*(?=\s+)', result_isis)
	listMPeer = re.findall(r'[a-zA-Z0-9\.-]+-M-[a-zA-Z0-9\.-]*(?=\s+)', result_isis)
	listXPeer = re.findall(r'[a-zA-Z0-9\.-]+-X-[a-zA-Z0-9\.-]*(?=\s+)', result_isis)
	nBPeer = len(set(listBPeer))
	nDPeer = len(set(listDPeer))
	nMPeer = len(set(listMPeer))
	nXPeer = len(set(listXPeer))
	listResult.append(nBPeer)
	listResult.append(nDPeer)
	listResult.append(nMPeer)
	listResult.append(nXPeer)

	if '-B-' in listResult[1]:
		if nBPeer < 1 and nDPeer >= 1:
			listResult.append('Only uT')
		elif nBPeer < 1 and nMPeer >= 1:
			listResult.append('Only uT')
		elif nBPeer >= 1 and nDPeer >= 1:
			listResult.append('OK')
		elif nBPeer >= 1 and nMPeer >= 1:
			listResult.append('OK')
		elif nBPeer >=1 and nDPeer < 1:
			listResult.append('Ony pT')
		elif nBPeer >=1 and nMPeer < 1:
			listResult.append('Ony pT')
		else:
			listResult.append('unknown')
	elif '-D-' in listResult[1]:
		if nMPeer >= 2 or nXPeer >= 2:
			listResult.append('OK')
		elif (nDPeer >= 1 and nMPeer >= 1) or (nDPeer >=1 and nXPeer >= 1):
			listResult.append('OK')
		elif nDPeer >=1 and nMPeer < 1:
			listResult.append('Only pT')
		elif nDPeer >= 1 and nXPeer < 1:
			listResult.append('Only pT')
		elif nDPeer < 1 and nMPeer < 2:
			listResult.append('Only uT')
		elif nDPeer < 1 and nXPeer < 2:
			listResult.append('Only uT')
		else:
			listResult.append('unknown')

	return listResult
	
def ZTE_B(child):
	content = []
	loginprompt = '[#>]'
	child.sendline('show isis adjacency')
	index = child.expect(['[mMore]',loginprompt])
	while index == 0:
		content += child.before
		child.send(' ')
		index = child.expect(['[mMore]',loginprompt])
	content = child.before
	result_isis = content

	global listResult
	listBPeer = re.findall(r'[a-zA-Z0-9\.-]+-B-[a-zA-Z0-9\.-]*(?=\s+)', result_isis)
	listDPeer = re.findall(r'[a-zA-Z0-9\.-]+-D-[a-zA-Z0-9\.-]*(?=\s+)', result_isis)
	listMPeer = re.findall(r'[a-zA-Z0-9\.-]+-M-[a-zA-Z0-9\.-]*(?=\s+)', result_isis)
	listXPeer = re.findall(r'[a-zA-Z0-9\.-]+-X-[a-zA-Z0-9\.-]*(?=\s+)', result_isis)
	nBPeer = len(set(listBPeer))
	nDPeer = len(set(listDPeer))
	nMPeer = len(set(listMPeer))
	nXPeer = len(set(listXPeer))
	listResult.append(nBPeer)
	listResult.append(nDPeer)
	listResult.append(nMPeer)
	listResult.append(nXPeer)

	if '-B-' in listResult[1]:
		if nBPeer < 1 and nDPeer >= 1:
			listResult.append('Only uT')
		elif nBPeer < 1 and nMPeer >= 1:
			listResult.append('Only uT')
		elif nBPeer >= 1 and nDPeer >= 1:
			listResult.append('OK')
		elif nBPeer >= 1 and nMPeer >= 1:
			listResult.append('OK')
		elif nBPeer >=1 and nDPeer < 1:
			listResult.append('Ony pT')
		elif nBPeer >=1 and nMPeer < 1:
			listResult.append('Ony pT')
		else:
			listResult.append('unknown')
	elif '-D-' in listResult[1]:
		if nMPeer >= 2 or nXPeer >= 2:
			listResult.append('OK')
		elif (nDPeer >= 1 and nMPeer >= 1) or (nDPeer >=1 and nXPeer >= 1):
			listResult.append('OK')
		elif nDPeer >=1 and nMPeer < 1:
			listResult.append('Only pT')
		elif nDPeer >= 1 and nXPeer < 1:
			listResult.append('Only pT')
		elif nDPeer < 1 and nMPeer < 2:
			listResult.append('Only uT')
		elif nDPeer < 1 and nXPeer < 2:
			listResult.append('Only uT')
		else:
			listResult.append('unknown')
	return listResult

def Fiber_B(child):
	loginprompt = '[#>]'
	child.send('show clns is-neighbors\r\n')
	child.expect('show clns is-neighbors\r\n')
	child.send('\r\n')
	child.expect(loginprompt)
	result_isis = child.before

	global listResult
	listBPeer = re.findall(r'[a-zA-Z0-9\.-]+-B-[a-zA-Z0-9\.-]*(?=\s+)', result_isis)
	listDPeer = re.findall(r'[a-zA-Z0-9\.-]+-D-[a-zA-Z0-9\.-]*(?=\s+)', result_isis)
	listMPeer = re.findall(r'[a-zA-Z0-9\.-]+-M-[a-zA-Z0-9\.-]*(?=\s+)', result_isis)
	listXPeer = re.findall(r'[a-zA-Z0-9\.-]+-X-[a-zA-Z0-9\.-]*(?=\s+)', result_isis)
	nBPeer = len(set(listBPeer))
	nDPeer = len(set(listDPeer))
	nMPeer = len(set(listMPeer))
	nXPeer = len(set(listXPeer))
	listResult.append(nBPeer)
	listResult.append(nDPeer)
	listResult.append(nMPeer)
	listResult.append(nXPeer)

	if '-B-' in listResult[1]:
		if nBPeer < 1 and nDPeer >= 1:
			listResult.append('Only uT')
		elif nBPeer < 1 and nMPeer >= 1:
			listResult.append('Only uT')
		elif nBPeer >= 1 and nDPeer >= 1:
			listResult.append('OK')
		elif nBPeer >= 1 and nMPeer >= 1:
			listResult.append('OK')
		elif nBPeer >=1 and nDPeer < 1:
			listResult.append('Ony pT')
		elif nBPeer >=1 and nMPeer < 1:
			listResult.append('Ony pT')
		else:
			listResult.append('unknown')
	elif '-D-' in listResult[1]:
		if nMPeer >= 2 or nXPeer >= 2:
			listResult.append('OK')
		elif (nDPeer >= 1 and nMPeer >= 1) or (nDPeer >=1 and nXPeer >= 1):
			listResult.append('OK')
		elif nDPeer >=1 and nMPeer < 1:
			listResult.append('Only pT')
		elif nDPeer >= 1 and nXPeer < 1:
			listResult.append('Only pT')
		elif nDPeer < 1 and nMPeer < 2:
			listResult.append('Only uT')
		elif nDPeer < 1 and nXPeer < 2:
			listResult.append('Only uT')
		else:
			listResult.append('unknown')
	return listResult


loginprompt = '[#>]'

try:
	loginIp = []
	conn = MySQLdb.connect(host='192.168.132.130',user='root',passwd='123456Qw!',port=3306)
	cur = conn.cursor()
	conn.select_db('IPRAN')
	sql = 'select * from bdcsv'
	cur.execute(sql)
	result = cur.fetchall()
	for row in result:
		loginIp.append(row[1])
	#print loginIp
except MySQLdb.Error,e:
	print "Mysql Error %d: %s" % (e.args[0], e.args[1])

LoginError = connect.LoginError
c = connect.Connector('gdcwb','123456Qw!2')

result = []

resultDict = {}
for index, ip in enumerate(loginIp):
	listResult = []
	try:
		child , loginMode = c.connectIPRAN(ip)
		hostname = getHosename(child)

		if loginMode == '3A':
			listResult.append('3A')
		elif loginMode == 'Local':
			listResult.append('Local')

		listResult.append(hostname)

		if re.search(r'910|950',hostname):
			listResult.append('HW-A')
		elif re.search(r'CX600',hostname):
			listResult.append('HW-B/D')
			listResult = HW_B(child)
		elif re.search(r'6130|6150|6220',hostname):
			listResult.append('ZTE-A')
		elif re.search(r'9000',hostname):
			listResult.append('ZTE-B')
			listResult = ZTE_B(child)
		elif re.search(r'R835E|R820',hostname):
			listResult.append('Fiber-A')
		elif re.search(r'R8000',hostname):
			listResult.append('Fiber-B')
			listResult = Fiber_B(child)
		else:
			listResult.append('Unknown')

		resultDict[ip] = listResult
		
	except RuntimeError:
		print ip + ' telnet login failed, due to TIMEOUT or EOF'
		#listResult.append('NO')
		listResult = ['No','','','','','','','','']
		#print listResult
		resultDict[ip] = listResult
	except LoginError:
		print ip + ' cannot login in'
		print 'All Failed'
		#listResult.append('All Failed')
		listResult = ['All Failed','','','','','','','']
		resultDict[ip] = listResult
print resultDict
for key in resultDict:
    cur.execute('update bdcsv set Telnet = "%s",HostName = "%s", DeviceType = "%s", nBPeer = "%s", nDPeer = "%s", nMPeer = "%s", nXPeer = "%s", Error = "%s" where LoginIp = "%s"' % tuple(resultDict[key] + [key]))
cur.close()
conn.commit()
conn.close()