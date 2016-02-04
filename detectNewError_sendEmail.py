#!-*-coding:utf-8-*-
import pymysql
import sys
import os
import time
import re

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

import smtplib


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

try:
	errIp = []
	bdcsv_err_ip = []
	conn = pymysql.connect(host='localhost', user='gdnoc', passwd='123456Qw!', db='ipran', port=3306)
	cur = conn.cursor()
	
	sql = 'select * from bdcsv b where b.Error = "unknown" or b.Error = ""'
	cur.execute(sql)
	sqlResult = cur.fetchall()
	for row in sqlResult:
		errIp.append(row[1])

	sql_err = 'select * from bdcsv_err'
	cur.execute(sql_err)
	sqlResult_err = cur.fetchall()
	for row in sqlResult_err:
		bdcsv_err_ip.append(row[1])

	newIp = []
	deleteIp = []

	for ip in errIp:
		if ip not in bdcsv_err_ip:
			status = 'NEW'
			cur.execute('insert into bdcsv_err (loginIp, status) VALUES ("%s","%s") '% (ip,status))
			newIp.append(ip)
		elif ip in bdcsv_err_ip:
			cur.execute('select status from bdcsv_err be where be.loginIp = "%s"' % ip)
			tmpResult = cur.fetchall()
			status = tmpResult[0][0]
			if status == 'NEW':
				status = 'EXISTS'
				cur.execute('update bdcsv_err set status = "%s" where loginIp = "%s" '% (status,ip))
			elif status == 'DELETE':
				status = 'NEW'
				newIp.append(ip)
				cur.execute('update bdcsv_err set status = "%s" where loginIp = "%s" '% (status,ip))

	for ip in bdcsv_err_ip:
		if ip not in errIp:
			cur.execute('select status from bdcsv_err be where be.loginIp = "%s"' % ip)
			tmpResult = cur.fetchall()
			status = tmpResult[0][0]
			if status != 'DELETE':
				status = 'DELETE'
				deleteIp.append(ip)
				cur.execute('update bdcsv_err set status = "%s" where loginIp = "%s" '% (status,ip))


	countOfNewIp = len(newIp)
	countOfDeleteIp = len(deleteIp)

	a = '''Now detected some devices cannot be logined in at %s, please try to solve them!
		Loopback: 
	''' % time.ctime()
	b = '''These devices have been solved.
		Loopback:
	'''
	c = '\r\n'.join(newIp)
	d = '\r\n'.join(deleteIp)

	if countOfNewIp != 0 or countOfDeleteIp != 0:
		from_addr = 'chengwb@189.cn'
		# change the password
		password = '******'
		to_addr = 'chengwb@189.cn'
		smtp_server = 'smtp.189.cn'
		if countOfNewIp !=0 and countOfDeleteIp != 0:
			msg = MIMEText(a+c+'\r\n'+b+d, 'plain', 'utf-8')
		elif countOfNewIp !=0:
			msg = MIMEText(a+c, 'plain', 'utf-8')
		else:
			msg = MIMEText(b+d, 'plain', 'utf-8')
		msg['From'] = _format_addr('系统管理员<%s>' % from_addr)
		msg['To'] = _format_addr('工程师<%s>' % to_addr)
		msg['Subject'] = Header('设备登陆状况变更', 'utf-8').encode()
		
		server = smtplib.SMTP(smtp_server, 25)
		server.set_debuglevel(1)
		server.login(from_addr, password)
		server.sendmail(from_addr, [to_addr], msg.as_string())
		server.quit()

	cur.close()
	conn.commit()
	conn.close()
except pymysql.Error as e:
	print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
except Exception as e:
	print(e)