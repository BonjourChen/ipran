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
			self.Username = raw_input("username:")
			self.Password = raw_input("password:")

	def connectIPRAN(self,strLoginIp):

		loginprompt = '[#>]'
		child = pexpect.spawn('telnet %s' %strLoginIp)
		child.logfile_read = sys.stdout

		index = child.expect(["[Uu]sername", pexpect.EOF, pexpect.TIMEOUT])
		if index == 1 or index == 2:
			raise RuntimeError, strLoginIp +' telnet login failed, due to TIMEOUT or EOF'
		child.sendline(self.Username)
		index = child.expect(["[pP]assword", pexpect.EOF, pexpect.TIMEOUT])
		if index == 0:
		# if index == 1 or index == 2:
		# 	child.send('\r\n')
		# 	index_p = child.expect(["[pP]assword", pexpect.EOF, pexpect.TIMEOUT])
		# 	child.send(self.Password + '\r\n')
		# else:
			child.sendline(self.Password)
			index = child.expect([loginprompt,'(?i)error','No username'])

			if index == 0: 
				loginInfo = child.before
				# hostname = re.search(r'(?<=\<)[a-zA-Z0-9\.-]*',loginInfo).group()
				loginMode = '3A'
				return child,loginMode
			elif index == 1 or index ==2:
				index_1 = child.expect(["[Uu]sername", pexpect.EOF, pexpect.TIMEOUT])
				if index_1 == 1 or index_1 == 2:
					#print ip +' telnet login failed, due to TIMEOUT or EOF'
					raise RuntimeError, strLoginIp +' telnet login failed, due to TIMEOUT or EOF'
				child.sendline('noc189')
				index_1 = child.expect(["[pP]assword", pexpect.EOF, pexpect.TIMEOUT])
				child.sendline('1qaz#EDC')
				index_1 = child.expect([loginprompt,'(?i)error','No username'])

				if index_1 == 0:
					loginInfo = child.before
					# hostname = re.search(r'(?<=\<)[a-zA-Z0-9\.-]*',loginInfo).group()
					loginMode = 'Local'
					return child,loginMode
				elif index_1 == 1 or index ==2:
					index_2 = child.expect(["[Uu]sername", pexpect.EOF, pexpect.TIMEOUT])
					if index_2 == 1 or index_2 == 2:
						#print ip +' telnet login failed, due to TIMEOUT or EOF'
						raise RuntimeError, strLoginIp +' telnet login failed, due to TIMEOUT or EOF'
					child.sendline('noc189')
					index_2 = child.expect(["[pP]assword", pexpect.EOF, pexpect.TIMEOUT])
					child.sendline('ipranv587!')
					index_2 = child.expect([loginprompt,'(?i)error','No username'])
					if index_2 == 0:
						loginInfo = child.before
						# hostname = re.search(r'(?<=\<)[a-zA-Z0-9\.-]*',loginInfo).group()
						loginMode = 'Local'
						return child,loginMode
					else:
						child.close(force=True)
						child = pexpect.spawn('telnet %s' %strLoginIp)
						child.logfile_read = sys.stdout
						index_3 = child.expect(["[Uu]sername", pexpect.EOF, pexpect.TIMEOUT])
						if index_3 == 1 or index_3 == 2:
							raise RuntimeError, strLoginIp +' telnet login failed, due to TIMEOUT or EOF'
						child.sendline('noc189')
						index_3 = child.expect(["[pP]assword", pexpect.EOF, pexpect.TIMEOUT])
						child.sendline('ipran4Ggood')
						index_3 = child.expect([loginprompt,'(?i)error','No username'])
						if index_3 == 0:
							loginInfo = child.before
							# hostname = re.search(r'(?<=\<)[a-zA-Z0-9\.-]*',loginInfo).group()
							loginMode = 'Local'
							return child,loginMode
						else:
							child.close(force=True)
							#print ip +' telnet login failed, due to TIMEOUT or EOF'
							raise LoginError

		else:
			child.send('\r\n')
			index_p = child.expect(["[pP]assword", pexpect.EOF, pexpect.TIMEOUT])
			child.send(self.Password + '\r\n')
			index = child.expect([loginprompt,'(?i)error','No username'])

			if index == 0: 
				loginInfo = child.before
				loginMode = '3A'
				return child,loginMode
			elif index == 1 or index ==2:
				index_1 = child.expect(["[Uu]sername", pexpect.EOF, pexpect.TIMEOUT])
				if index_1 == 1 or index_1 == 2:
					raise RuntimeError, strLoginIp +' telnet login failed, due to TIMEOUT or EOF'
				child.send('noc189\r\n')
				index_1 = child.expect(["[pP]assword", pexpect.EOF, pexpect.TIMEOUT])
				child.sendline('1qaz#EDC\r\n')
				index_1 = child.expect([loginprompt,'(?i)error','No username'])

				if index_1 == 0:
					loginInfo = child.before
					loginMode = 'Local'
					return child,loginMode
				elif index_1 == 1 or index ==2:
					index_2 = child.expect(["[Uu]sername", pexpect.EOF, pexpect.TIMEOUT])
					if index_2 == 1 or index_2 == 2:
						raise RuntimeError, strLoginIp +' telnet login failed, due to TIMEOUT or EOF'
					child.send('noc189\r\n')
					index_2 = child.expect(["[pP]assword", pexpect.EOF, pexpect.TIMEOUT])
					child.send('ipranv587!\r\n')
					index_2 = child.expect([loginprompt,'(?i)error','No username'])
					if index_2 == 0:
						loginInfo = child.before
						loginMode = 'Local'
						return child,loginMode
					else:
						child.close(force=True)
						child = pexpect.spawn('telnet %s' %strLoginIp)
						child.logfile_read = sys.stdout
						index_3 = child.expect(["[Uu]sername", pexpect.EOF, pexpect.TIMEOUT])
						if index_3 == 1 or index_3 == 2:
							raise RuntimeError, strLoginIp +' telnet login failed, due to TIMEOUT or EOF'
						child.send('noc189\r\n')
						index_3 = child.expect(["[pP]assword", pexpect.EOF, pexpect.TIMEOUT])
						child.send('ipran4Ggood\r\n')
						index_3 = child.expect([loginprompt,'(?i)error','No username'])
						if index_3 == 0:
							loginInfo = child.before
							loginMode = 'Local'
							return child,loginMode
						else:
							child.close(force=True)
							raise LoginError
