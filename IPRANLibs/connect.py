#!-*-coding:utf-8-*-
import pexpect
import os
import sys
import re

class LoginError(Exception):
	pass

class Connector(object):

	def __init__(self, *tupleInfo):
		if tupleInfo:
			self.Username = tupleInfo[0]
			self.Password = tupleInfo[1]
		else:
			self.Username = input("username:")
			self.Password = input("password:")

	def connectIPRAN(self,strLoginIp):
		loginprompt = '[#>]'
		child = pexpect.spawn('telnet %s' % strLoginIp)
		index = child.expect(['[Uu]sername', pexpect.EOF, pexpect.TIMEOUT],30)
		if index == 1 or index == 2:
			loginMode = 'No'
			child.close(force=True)
			return child,loginMode
		elif index == 0:
			child.send(self.Username + '\r')
			index = child.expect(["[pP]assword", pexpect.EOF, pexpect.TIMEOUT],30)
			child.send(self.Password + '\r')
			index = child.expect([loginprompt,'(?i)error','No username','Bad passwords', pexpect.EOF, pexpect.TIMEOUT],30)
			if index == 0: 
				loginInfo = child.before
				loginMode = '3A'
				return child,loginMode
			else:
				index_1 = child.expect(["[Uu]sername", pexpect.EOF, pexpect.TIMEOUT],30)
				if index_1 == 1 or index_1 == 2:
					loginMode = 'Failed'
					return child,loginMode
				elif index_1 ==0:
					child.send('noc189\r')
					index_1 = child.expect(["[pP]assword", pexpect.EOF, pexpect.TIMEOUT],30)
					child.send('1qaz#EDC\r')
					index_1 = child.expect([loginprompt,'(?i)error','No username','Bad passwords', pexpect.EOF, pexpect.TIMEOUT],30)
					if index_1 == 0:
						loginInfo = child.before
						loginMode = 'Local'
						return child,loginMode
					else:
						index_2 = child.expect(["[Uu]sername", pexpect.EOF, pexpect.TIMEOUT],30)
						if index_2 == 1 or index_2 == 2:
							loginMode = 'Failed'
							child.close(force=True)
							return child,loginMode
						elif index_2 == 0:
							child.send('noc189\r')
							index_2 = child.expect(["[pP]assword", pexpect.EOF, pexpect.TIMEOUT],30)
							child.send('ipranv587!\r')
							index_2 = child.expect([loginprompt,'(?i)error','No username','Bad passwords', pexpect.EOF, pexpect.TIMEOUT],30)
							if index_2 == 0:
								loginInfo = child.before
								loginMode = 'Local'
								return child,loginMode
							else:
								child.close(force=True)
								child = pexpect.spawn('telnet %s' %strLoginIp)
								index_3 = child.expect(["[Uu]sername", pexpect.EOF, pexpect.TIMEOUT],30)
								if index_3 == 1 or index_3 == 2:
									loginMode = 'No'
									return child,loginMode
								child.send('noc189\r')
								index_3 = child.expect(["[pP]assword", pexpect.EOF, pexpect.TIMEOUT],30)
								child.send('ipran4Ggood\r')
								index_3 = child.expect([loginprompt,'(?i)error','No username', pexpect.EOF, pexpect.TIMEOUT],30)
								if index_3 == 0:
									loginInfo = child.before
									loginMode = 'Local'
									return child,loginMode
								else:
									child.close(force=True)
									loginMode = 'Failed'
									return child,loginMode