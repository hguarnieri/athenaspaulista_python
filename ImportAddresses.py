import re
import urllib2
import MySQLdb

# Functions
def remove_tags(data):
    p = re.compile(r'<[^<]*?>')
    return p.sub('', data)

db = MySQLdb.connect(host="localhost",
                     user="root",
                     passwd="123456",
                     db="athenas",
                     charset='utf8')

cur = db.cursor()

for numero in range(1, 70):

    numeroLinha = str(numero).zfill(2)
    url = 'http://www.athenaspaulista.com.br/LINHAS/Linha' + numeroLinha + '.htm'
    timeToGo = ''
    timeToGoBack = ''

    # Correcoes
    whereToSplit = [2, 4, 6]
    if numero == 44 or numero == 52:
        whereToSplit = [2, 3, 4]

    whereToSplitTitle = "-"
    if numero == 58 or numero == 41:
        whereToSplitTitle = "\xe2\x80\x93"

    divider = ";"
    if numero == 60:
        divider = ","

    # Delete old values
    cur.execute("DELETE FROM enderecos WHERE linha=" + numeroLinha)

    try:
        response = urllib2.urlopen(url)
        html = response.read().decode('windows-1252').encode('utf-8').replace("&nbsp;", "").replace('\r\n', '').replace("	", "").replace("  ", " ")

        unclearedTitle = html.split('<tr style=\'mso-yfti-irow:0;mso-yfti-firstrow:yes;mso-yfti-lastrow:yes\'>')[whereToSplit[0]].split("</tr>")[0]
        title = remove_tags(unclearedTitle).split(whereToSplitTitle, 1)[1].strip()

        print title

        unclearedAddressesToGo = html.split('<tr style=\'mso-yfti-irow:0;mso-yfti-firstrow:yes;mso-yfti-lastrow:yes\'>')[whereToSplit[1]].split("</tr>")[0]
        if numero == 44:
            unclearedAddressesToGo = unclearedAddressesToGo.split("<p class=MsoPlainText style='text-align:justify'>")[2].split("</p>")[0]
        if numero == 60:
            unclearedAddressesToGo = unclearedAddressesToGo.split(")", 1)[1]
        addressesToGo = remove_tags(unclearedAddressesToGo).strip()
        print addressesToGo

        ordem = 0
        for address in addressesToGo.split(divider):
            if address[-1] == '.':
                address = address[-1:]
            if len(address) > 3:
                cur.execute("INSERT INTO enderecos VALUES(%s, %s, %s, %s)", (numeroLinha, ordem, 1, address.strip()))
                ordem += 1

        try:
            unclearedAddressesToGoBack = html.split('<tr style=\'mso-yfti-irow:0;mso-yfti-firstrow:yes;mso-yfti-lastrow:yes\'>')[whereToSplit[2]].split("</tr>")[0]
            if numero == 44:
                unclearedAddressesToGoBack = unclearedAddressesToGoBack.split("<p class=MsoPlainText style='text-align:justify'>")[2].split("</p>")[0]
            if numero == 60:
                unclearedAddressesToGoBack = unclearedAddressesToGoBack.split(")", 1)[1]
            addressesToGoBack = remove_tags(unclearedAddressesToGoBack).strip()

            print addressesToGoBack

            ordem = 0
            for address in addressesToGo.split(divider):
                if address[-1] == '.':
                    address = address[-1:]
                if len(address) > 3:
                    cur.execute("INSERT INTO enderecos VALUES(%s, %s, %s, %s)", (numeroLinha, ordem, 2, address.strip()))
                    ordem += 1
        except Exception, e:
            print ''

    except urllib2.HTTPError, err:
        if err.code == 404:
            print "Linha " + numeroLinha + " nao encontrada."
    except:
        print "Erro na linha: " + numeroLinha

    db.commit()

# Cleanings
cur.execute("UPDATE enderecos SET endereco = TRIM(endereco)")

cur.close()
