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
		
