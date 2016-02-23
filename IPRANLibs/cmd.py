#!-*-coding:utf-8-*-
import pexpect
import os
import sys
import re

def cmd_show(child,command,more,stop,timeout=3):
	child.send(command + '\r')
	show_result = ''
	index = child.expect([command,pexpect.TIMEOUT])
	if index == 0:
		while True:
			index_1 = child.expect([more,stop,pexpect.TIMEOUT])
			show_result += str(child.before, encoding = 'utf-8')
			if index_1 == 0:
				child.send(' ')
			else:
				break
	elif index == 1:
		pass
	return show_result

def cmd_telnet(child,ip):
	loginprompt = '[#>]'
	command = 'telnet '+ ip
	child.send(command+'\r')
	index = child.expect(['[Uu]sername',pexpect.EOF,pexpect.TIMEOUT],30)
	if index == 0:
		child.send('gdcwb'+'\r')
		index_1 = child.expect(['[Pp]assword',pexpect.EOF,pexpect.TIMEOUT],30)
		if index_1 == 0:
			child.send('123456Qw!2'+'\r')
			index_2 = child.expect([loginprompt,'(?i)error','No username', pexpect.EOF, pexpect.TIMEOUT],30)
			if index_2 == 0:
				loginMode = '3A'
				return child,loginMode
			else:
				index_3 = child.expect(["[Uu]sername", pexpect.EOF, pexpect.TIMEOUT],30)
				if index_3 == 0:
					child.send('noc189'+'\r')
					index_4 = child.expect(["[pP]assword", pexpect.EOF, pexpect.TIMEOUT],30)
					if index_4 == 0:
						child.send('1qaz#EDC'+'\r')
						index_5 = child.expect([loginprompt,'(?i)error','No username', pexpect.EOF, pexpect.TIMEOUT],30)
						if index_5 == 0:
							loginMode = 'Local'
							return child,loginMode
						else:
							loginMode = 'Failed'
							return child,loginMode
				else:
					loginMode = 'No'
					return child,loginMode
		else:
			loginMode = 'No'
			return child,loginMode
	else:
		loginMode = 'No'
		return child,loginMode



		
