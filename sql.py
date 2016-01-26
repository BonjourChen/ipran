import MySQLdb
import os
import sys
import re

try:
    loginIp = []
    conn = MySQLdb.connect(host='192.168.138.131',user='root',passwd='123456Qw!',port=3306)
    cur = conn.cursor()
    conn.select_db('IPRAN')
    sql = 'select * from bdcsv'
    cur.execute(sql)
    result = cur.fetchall()
    for row in result:
        loginIp.append(row[1])
    print loginIp
except MySQLdb.Error,e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])
