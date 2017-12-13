from flask import Flask,flash, render_template, request
from beebotte import *
from pymongo import MongoClient
app = Flask(__name__)
app.secret_key = 'some_secret'
flag=1
client = MongoClient()
db = client.test
@app.route('/')
def home():
    db = client.test
    cursor = db.numbers.find()
    return render_template('home.html',cursor=cursor,av=0, umbral=0)

@app.route('/media',methods = ['POST', 'GET'])
def average():
    global flag
    if request.method == 'POST':
        suma=0
        cantidad=0
        if flag == 1:
            cursor = db.numbers.find()
            for document in cursor:
                suma=suma+document["number"]
                cantidad=cantidad+1
            media=suma/cantidad
            data_base="MongoDB"
            flag=0
        else:
            _hostname   = 'api.beebotte.com'
            _token      = '1510099700783_0F8OPqJwsCC25m20'
            bbt = BBT(token = _token, hostname = _hostname)
            records = bbt.read("Numbers_Database", "numbers", limit = 200)
            for document in records:
                suma=suma+document["data"]
                cantidad=cantidad+1
            media=suma/cantidad
            data_base="Beebotte"
            flag=1
        cursor = db.numbers.find()
        return render_template('home.html',cursor=cursor,av=1, umbral=0, media=media,data_base=data_base)
@app.route('/umbral',methods = ['POST', 'GET'])
def umbral():
    if request.method == 'POST':
        umbral_minimo = request.form['umbral_minimo']
        umbral_maximo = request.form['umbral_maximo']        
        if len(str(umbral_minimo))==0:
            umbral_minimo=0
        if len(str(umbral_maximo))==0:
            umbral_maximo=100
        cursor = db.numbers.find({"number": {"$gt": float(umbral_minimo), "$lt":float(umbral_maximo)}})
        i=0
        for document in cursor:
            i=i+1
        cursor = db.numbers.find({"number": {"$gt": float(umbral_minimo), "$lt":float(umbral_maximo)}})
        ultimo_numero=document["number"]
        ultima_hora=document["hour"]
        ultima_fecha=document["date"]
        return render_template('home.html',cursor=cursor,av=0,umbral=1,ultimo_numero=ultimo_numero,ultima_hora=ultima_hora,ultima_fecha=ultima_fecha)
@app.route('/about')
def about():
  return render_template('about.html')

  
if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
