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
    whereToSplit = [2, 3, 5]
    if numero == 44 or numero == 52:
        whereToSplit = [2, 3, 4]

    whereToSplitTitle = "-"
    if numero == 58 or numero == 41:
        whereToSplitTitle = "\xe2\x80\x93"

    # Delete old values
    cur.execute("DELETE FROM linhas WHERE numero=" + numeroLinha)

    try:
        response = urllib2.urlopen(url)
        html = response.read().decode('windows-1252').encode('utf-8').replace("&nbsp;", "").replace('\r\n', '').replace("	", "")

        unclearedTitle = html.split('<tr style=\'mso-yfti-irow:0;mso-yfti-firstrow:yes;mso-yfti-lastrow:yes\'>')[whereToSplit[0]].split("</p>")[0]
        title = remove_tags(unclearedTitle).split(whereToSplitTitle, 1)[1].strip()

        unclearedTimeToGo = html.split('<tr style=\'mso-yfti-irow:0;mso-yfti-firstrow:yes;mso-yfti-lastrow:yes\'>')[whereToSplit[1]].split("</p>")[0]
        timeToGo = remove_tags(unclearedTimeToGo).strip()

        try:
            unclearedTimeToGoBack = html.split('<tr style=\'mso-yfti-irow:0;mso-yfti-firstrow:yes;mso-yfti-lastrow:yes\'>')[whereToSplit[2]].split("</p>")[0]
            timeToGoBack = remove_tags(unclearedTimeToGoBack).strip()
        except:
            timeToGoBack = '-'

        if len(timeToGo) < 5:
            timeToGo = '-'

        if len(timeToGoBack) < 7:
            timeToGoBack = '-'

        print title
        print timeToGo
        print timeToGoBack
        print "\n"

        cur.execute("INSERT INTO linhas VALUES(%s, %s, %s, %s, %s)", (numeroLinha, title, url, timeToGo, timeToGoBack))
    except urllib2.HTTPError, err:
        if err.code == 404:
            print "Linha " + numeroLinha + " nao encontrada"
    except Exception, e:
        print "Erro na linha: " + numeroLinha + " " + str(e)

    db.commit()

cur.close()
