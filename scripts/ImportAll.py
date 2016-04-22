#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import urllib2
from pymongo import MongoClient

# Functions
def remove_tags(replaceS, data):
	p = re.compile(r'<[^<]*?>')
	return p.sub(replaceS, data)

def isTime(value):
	try:
		re.search('[0-9]{2}[:][0-9]{2}', value).group(0)
		return True
	except:
		return False

def parseTimes(data):
	times = []
	clearList = filter(None, data.split("<tag>"))

	i = 0
	while i < len(clearList):

		if i == 0 and "n\xc3\x83o opera" in clearList[i].lower():
			return times

		p = clearList[i]
		if i == (len(clearList) - 1):
			times.append([p, "-"])
		else:
			time = isTime(clearList[i+1])
			if time:
				times.append([p, clearList[i+1]])
				i += 1
			else:
				times.append([p, "-"])

		i += 1

	return times

def readLinha(html, numero, title, url):
	whereToSplit = [2, 3, 5]
	if numero == 44 or numero == 52:
		whereToSplit = [2, 3, 4]

	unclearedTimeToGo = html.split('<tr style=\'mso-yfti-irow:0;mso-yfti-firstrow:yes;mso-yfti-lastrow:yes\'>')[whereToSplit[1]].split("</p>")[0]
	timeToGo = remove_tags('', unclearedTimeToGo).strip()

	try:
		unclearedTimeToGoBack = html.split('<tr style=\'mso-yfti-irow:0;mso-yfti-firstrow:yes;mso-yfti-lastrow:yes\'>')[whereToSplit[2]].split("</p>")[0]
		timeToGoBack = remove_tags('', unclearedTimeToGoBack).strip()
	except:
		timeToGoBack = '-'

	if len(timeToGo) < 5:
		timeToGo = '-'
	if len(timeToGoBack) < 7:
		timeToGoBack = '-'

	return { "number": numero, "title": title, "url": url, "timeToGo": timeToGo, "timeToGoBack": timeToGoBack }

def readAddresses(html, numero):
	whereToSplit = [2, 4, 6]
	if numero == 44 or numero == 52:
		whereToSplit = [2, 3, 4]

	divider = ";"
	if numero == 60:
		divider = ","
	unclearedAddressesToGo = html.split('<tr style=\'mso-yfti-irow:0;mso-yfti-firstrow:yes;mso-yfti-lastrow:yes\'>')[whereToSplit[1]].split("</tr>")[0]
	if numero == 44:
		unclearedAddressesToGo = unclearedAddressesToGo.split("<p class=MsoPlainText style='text-align:justify'>")[2].split("</p>")[0]
	if numero == 60:
		unclearedAddressesToGo = unclearedAddressesToGo.split(")", 1)[1]
	addressesToGo = remove_tags('', unclearedAddressesToGo).strip()
	
	addressesGo = []
	addressesGoBack = []
	ordem = 0
	for address in addressesToGo.split(divider):
		if address[-1] == '.':
			address = address[-1:]
		if len(address) > 3:
			addressesGo.append({ "order": ordem, "address": address.strip() })
			ordem += 1

	try:
		unclearedAddressesToGoBack = html.split('<tr style=\'mso-yfti-irow:0;mso-yfti-firstrow:yes;mso-yfti-lastrow:yes\'>')[whereToSplit[2]].split("</tr>")[0]
		if numero == 44:
			unclearedAddressesToGoBack = unclearedAddressesToGoBack.split("<p class=MsoPlainText style='text-align:justify'>")[2].split("</p>")[0]
		if numero == 60:
			unclearedAddressesToGoBack = unclearedAddressesToGoBack.split(")", 1)[1]
		addressesToGoBack = remove_tags('', unclearedAddressesToGoBack).strip()

		ordem = 0
		for address in addressesToGo.split(divider):
			if address[-1] == '.':
				address = address[-1:]
			if len(address) > 3:
				addressesGoBack.append({ "order": ordem, "address": address.strip() })
				ordem += 1
	except Exception as e:
		print e

	return addressesGo, addressesGoBack

def readTimes(html, numero):
	try:		
		util = "DIAS ÚTEIS"
		if numero == 34:
			util = "DIA ÚTEIS"
		clearHtml = remove_tags('<tag>', html).strip()

		times = {}
 
		if numero == 52:
			holidays = clearHtml.split("FERIADOS")
			times["holidays"] = parseTimes(holidays[1])
			sundays = holidays[0].split("DOMINGOS")
		else:
			sundays = clearHtml.split("DOMINGOS E FERIADOS") # [1]

		if len(sundays) == 1:
			sundays = clearHtml.split("DOMINGO E FERIADOS") # [1]

		if len(sundays) == 1:
			sundays = clearHtml.split("DOMINGO E FERIADO") # [1]

		saturdays = sundays[0].split("SÁBADOS") # [1]

		if len(saturdays) == 1:
			saturdays = sundays[0].split("SÁBADO") # [1]

		allDays = saturdays[0].split(util) # [1]
		
		times["sundays"] = parseTimes(sundays[1])
		times["saturdays"] = parseTimes(saturdays[1])
		times["days"] = parseTimes(allDays[1])

		return times
	except Exception as e:
		print e

excludes = [18, 23, 27, 38, 39, 40, 45, 51, 54, 55]

linhas = []
for numero in range(1, 70):

	numeroLinha = str(numero).zfill(2)
	url = 'http://www.athenaspaulista.com.br/LINHAS/Linha' + numeroLinha + '.htm'

	# Correcoes
	whereToSplitTitle = "-"
	if numero == 58 or numero == 41:
		whereToSplitTitle = "\xe2\x80\x93"

	try:
		response = urllib2.urlopen(url)
		html = response.read().decode('windows-1252').encode('utf-8').replace("&nbsp;", "").replace('\r\n', '').replace("	", "").replace("  ", " ").replace("\xc2\xa0", "")

		unclearedTitle = html.split('<tr style=\'mso-yfti-irow:0;mso-yfti-firstrow:yes;mso-yfti-lastrow:yes\'>')[2].split("</tr>")[0]
		title = remove_tags('', unclearedTitle).split(whereToSplitTitle, 1)[1].strip()

		print str(numero) + ": " + title + "\n"

		linha = readLinha(html, numero, title, url)
		addr = readAddresses(html, numero)

		linha["addressesToGo"] = addr[0]
		linha["addressesToGoBack"] = addr[1]

		if numero not in excludes:
			linha["times"] = readTimes(html, numero)

		linhas.append(linha)
	except urllib2.HTTPError as err:
		if err.code == 404:
			print "Linha " + numeroLinha + " nao encontrada."
	except Exception as err:
		print "Erro na linha: " + numeroLinha
		print err

client = MongoClient()
db = client.sancabus
db.routes.delete_many({})
db.routes.insert_many(linhas)
print db.routes.count()