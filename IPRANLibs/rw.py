#!-*-coding:utf-8-*-
import sys
import os
import csv
import re

def ReadFromTxt(strFileName, strFileDir = '.'):
	strFilePath = os.path.join(strFileDir, strFileName)
	if not os.path.exists(strFilePath):
		print(strFileName + ' file not found')
	else:
		listLines = []
		with open(strFilePath,'r') as txtFile:
			for line in txtFile:
				if not re.search(r'^\s*$',line):
					listLines.append(line.strip())
		return listLines

def WriteToTxt(strFileName, strData, strFileDir = '.'):
	strFilePath = os.path.join(strFileDir, strFileName)
	with open(strFilePath, 'a') as txtFile:
		txtFile.write(strData)

def ReadFromCsv(strFileName,strFileDir = '.'):
	strFilePath = os.path.join(strFileDir, strFileName)
	if not os.path.join(strFileDir + strFileName):
		print(strFileName + ' file not found')
	else:
		listLines = []
		with open(strFilePath, newline = '') as csvFile:
			reader = csv.reader(csvFile, delimiter = ' ', quotechar ='|')
			for row in reader:
				listLines.append(row)
		return listLines

def DictReadFromCsv(strFileName, strFileDir = '.'):
	strFilePath = os.path.join(strFileDir, strFileName)
	if not os.path.join(strFileDir + strFileName):
		print(strFileName + ' file not found')
	else:
		listLines = []
		with open(strFilePath) as csvFile:
			reader = csv.DictReader(csvFile)
			for row in reader:
				listLines.append(row)
		return listLines

def DictWriteToCsv(strFileName, fieldnames, strData, strFileDir = '.'):
	strFilePath = os.path.join(strFileDir, strFileName)
	if not os.path.join(strFileDir + strFileName):
		print(strFileName + ' file not found')
	else:
		with open(strFilePath, 'w') as csvFile:
			writer = csv.DictWriter(csvFile, fieldnames = fieldnames)
			writer.writeheader()
			writer.writerows(strData)
