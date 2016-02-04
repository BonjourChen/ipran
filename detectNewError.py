#!-*-coding:utf-8-*-
import pymysql
import sys
import os
import time
import re

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
				
	cur.close()
	conn.commit()
	conn.close()
except pymysql.Error as e:
	print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
except Exception as e:
	print(e)