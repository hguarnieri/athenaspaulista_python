#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import urllib2

# Functions
def remove_tags(data):
    p = re.compile(r'<[^<]*?>')
    return p.sub('<tag>', data)

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

for numero in range(53, 54):

    numeroLinha = str(numero).zfill(2)
    url = 'http://www.athenaspaulista.com.br/LINHAS/Linha' + numeroLinha + '.htm'

    # Correcoes
    whereToSplit = [2, 4, 6]
    if numero == 44 or numero == 52:
        whereToSplit = [2, 3, 4]

    whereToSplitTitle = "-"
    if numero == 58 or numero == 41:
        whereToSplitTitle = "\xe2\x80\x93"

    try:
        response = urllib2.urlopen(url)
        html = response.read().decode('windows-1252').encode('utf-8').replace("&nbsp;", "").replace('\r\n', '').replace("	", "").replace("  ", " ")

        unclearedTitle = html.split('<tr style=\'mso-yfti-irow:0;mso-yfti-firstrow:yes;mso-yfti-lastrow:yes\'>')[whereToSplit[0]].split("</tr>")[0]
        title = remove_tags(unclearedTitle).split(whereToSplitTitle, 1)[1].strip()

        print title + "\n"

        clearHtml = remove_tags(html).strip()
        sundays = clearHtml.split("DOMINGOS E FERIADOS") # [1]
        saturdays = sundays[0].split("SÁBADOS") # [1]
        allDays = saturdays[0].split("DIAS ÚTEIS") # [1]

        print "Dias úteis"
        print parseTimes(allDays[1])
        print "\n\n"

        print "Sábados"
        print parseTimes(saturdays[1])
        print "\n\n"

        print "Domingos e Feriados"
        print parseTimes(sundays[1])
        print "\n\n"

    except urllib2.HTTPError, err:
        if err.code == 404:
            print "Linha " + numeroLinha + " nao encontrada."
        print err
    except:
        print "Erro na linha: " + numeroLinha
