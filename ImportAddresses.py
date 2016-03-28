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

for numero in range(1, 71):

    numeroLinha = str(numero).zfill(2)
    url = 'http://www.athenaspaulista.com.br/LINHAS/Linha' + numeroLinha + '.htm'

    # Delete old values
    cur.execute("DELETE FROM enderecos WHERE linha=" + numeroLinha)

    try:
        response = urllib2.urlopen(url)
        html = response.read().decode('windows-1252').encode('utf-8')

        unclearedTitle = html.split('<tr style=\'mso-yfti-irow:0;mso-yfti-firstrow:yes;mso-yfti-lastrow:yes\'>')[2].split("</tr>")[0]
        title = remove_tags(unclearedTitle).split("-")[1].strip()

        print title

        unclearedAddressesToGo = html.split('<tr style=\'mso-yfti-irow:0;mso-yfti-firstrow:yes;mso-yfti-lastrow:yes\'>')[4].split("</tr>")[0]
        addressesToGo = remove_tags(unclearedAddressesToGo).strip().replace("\n", "")

        print addressesToGo

        ordem = 0
        for address in addressesToGo.split(";"):
            cur.execute("INSERT INTO enderecos VALUES(%s, %s, %s, %s)", (numeroLinha, ordem, 1, address))
            ordem += 1

        unclearedAddressesToGoBack = html.split('<tr style=\'mso-yfti-irow:0;mso-yfti-firstrow:yes;mso-yfti-lastrow:yes\'>')[6].split("</tr>")[0]
        addressesToGoBack = remove_tags(unclearedAddressesToGoBack).strip().replace("\n", "")

        print addressesToGoBack

        ordem = 0
        for address in addressesToGo.split(";"):
            cur.execute("INSERT INTO enderecos VALUES(%s, %s, %s, %s)", (numeroLinha, ordem, 2, address))
            ordem += 1

    except urllib2.HTTPError, err:
        if err.code == 404:
            print "Linha " + numeroLinha + " nao encontrada."
    except:
        print "Erro na linha: " + numeroLinha

    db.commit()

# Cleanings
cur.execute("UPDATE enderecos SET endereco = REPLACE(endereco, '\r', '')")
cur.execute("UPDATE enderecos SET endereco = REPLACE(endereco, '  ', ' ')")
cur.execute("UPDATE enderecos SET endereco = TRIM(endereco)")

cur.close()
