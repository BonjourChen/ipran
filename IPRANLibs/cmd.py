#!-*-coding:utf-8-*-
import pexpect
import os
import sys
import re

class cmd(object):
	def __init__(self):
		pass

	def cmd_show_HWZTE(child,commond,more,stop,timeout=3):
		self.child.sendline(commond)
		show_result = ''
		index = self.child.expect([commond,pexpect.TIMEOUT])
		if index == 0:
			while True:
				index_1 = self.child.expect([more,stop,pexpect.TIMEOUT])
				show_result += child.before
				if index_1 == 0:
					self.child.send(' ')
				else:
					break
		elif index == 1:
			pass
		return show_result
		
