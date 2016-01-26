#!-*-coding:utf-8-*-
import MySQLdb
import pexpect
import os
import sys
import re

reload(sys)
sys.setdefaultencoding('utf8')

ipaddress = '14.123.119.154'
ipaddress1 = '14.123.74.117'
loginUser = 'gdcwb'
password = '123456Qw!2'
loginprompt = '[$#>]'

cmd = 'telnet ' + ipaddress
child = pexpect.spawn(cmd)
index = child.expect(["[Uu]sername", pexpect.EOF, pexpect.TIMEOUT])
if index == 0:
	child.sendline(loginUser)
	index = child.expect(["[pP]assword", pexpect.EOF, pexpect.TIMEOUT])
	child.sendline(password)
	child.expect(loginprompt)
	if index == 0:
		child.sendline(' ')
		#child.sendline('dis isis peer')
		#index = child.expect('dis isis peer')
		#child.sendline(' ')
		child.expect('$>')
		print child.before
		#listBPeer = re.findall(r'[a-zA-Z0-9\.-]+-B-[a-zA-Z0-9\.-]*(?=\s+)', CMD_RESULT)
		#print ",".join(listBPeer)
	else:
		print "telnet login failed, due to TIMEOUT or EOF"
		child.close(force=True)
else:
	print "telnet login failed, due to TIMEOUT or EOF"
	child.close(force=True)

