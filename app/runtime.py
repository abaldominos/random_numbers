import urllib2
import re
import datetime
from pymongo import MongoClient
from beebotte import *
url = 'http://www.numeroalazar.com.ar/'

respuesta = urllib2.urlopen(url)
contenidoWeb = respuesta.read()


elemento=re.findall('\d?\d?\d[.]\d\d<br>', contenidoWeb)

formato_fecha="%d/%m/%y"
formato_hora="%H:%M"
fecha=datetime.datetime.utcnow()

client = MongoClient()
db = client.test
result = db.numbers.insert_one({"number" : float(elemento[0].strip('<br>')),"date" : fecha.strftime(formato_fecha),"hour" : fecha.strftime(formato_hora)})


_hostname   = 'api.beebotte.com'
_token      = '1510099700783_0F8OPqJwsCC25m20'
bbt = BBT(token = _token, hostname = _hostname)
bbt.write("Numbers_Database", "numbers", float(elemento[0].strip('<br>')))
bbt.write("Numbers_Database", "dates", str(fecha))
