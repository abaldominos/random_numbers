import urllib2

url = 'http://www.numeroalazar.com.ar/'

respuesta = urllib2.urlopen(url)
contenidoWeb = respuesta.read()
import re

#match_pattern = re.search('head', contenidoWeb)
#print match_pattern
elemento=re.findall('\d?\d?\d[.]\d\d<br>', contenidoWeb)
#with open('/home/user/flaskapp/app/dataBase.txt','a') as outFile:
#    outFile.write(elemento[0].strip('<br>')+'\n')
import datetime
fecha=datetime.datetime.utcnow()
from pymongo import MongoClient
client = MongoClient()
db = client.test
result = db.numbers.insert_one({"number" : float(elemento[0].strip('<br>')),"date" : fecha})
from beebotte import *

_hostname   = 'api.beebotte.com'
_token      = '1510099700783_0F8OPqJwsCC25m20'
bbt = BBT(token = _token, hostname = _hostname)
bbt.write("Numbers_Database", "numbers", float(elemento[0].strip('<br>')))
bbt.write("Numbers_Database", "dates", str(fecha))
