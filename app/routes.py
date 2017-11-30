from flask import Flask,flash, render_template, request
from beebotte import *
app = Flask(__name__)
app.secret_key = 'some_secret'
flag=1
@app.route('/')
def home():
    formato_hora="%H:%M"
    formato_fecha="%d/%m/%y"
    archivo = open("./templates/home.html", "w")
    archivo.write('{% extends "numbers_layout.html" %}\n{% block numbers %}\n')
    from pymongo import MongoClient
    client = MongoClient()
    db = client.test
    cursor = db.numbers.find()
    for document in cursor:
        archivo.write("<tr><td>"+str(document["number"])+"</td><td>"+str(document["date"].strftime(formato_hora))+"</td><td>"+str(document["date"].strftime(formato_fecha))+"</td></tr>")
    archivo.write("\n{% endblock %}\n")
    archivo.close() 
    return render_template('home.html')

@app.route('/media',methods = ['POST', 'GET'])
def average():
    global flag
    formato_hora="%H:%M"
    formato_fecha="%d/%m/%y"
    if request.method == 'POST':
        archivo = open("./templates/home.html", "w")
        archivo.write('{% extends "numbers_layout.html" %}\n{% block numbers %}\n')
        from pymongo import MongoClient
        client = MongoClient()
        db = client.test
        cursor = db.numbers.find()
        for document in cursor:
            archivo.write("<tr><td>"+str(document["number"])+"</td><td>"+str(document["date"].strftime(formato_hora))+"</td><td>"+str(document["date"].strftime(formato_fecha))+"</td></tr>")
        archivo.write("\n{% endblock %}\n")
        suma=0
        cantidad=0
        if flag == 1:
            cursor = db.numbers.find()
            for document in cursor:
                suma=suma+document["number"]
                cantidad=cantidad+1
            media=suma/cantidad
            archivo.write('{% block average %}\n<tr><td>La media calculada por MongoDB es '+str(media)+'</td></tr>\n{% endblock %}')
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
            archivo.write('{% block average %}\n<tr><td>La media calculada por Beebotte es '+str(media)+'</td></tr>\n{% endblock %}')
            flag=1
        archivo.close() 
        return render_template('home.html')
    else:
        return 'El umbral es de hola'
@app.route('/umbral',methods = ['POST', 'GET'])
def umbral():
    formato_hora="%H:%M"
    formato_fecha="%d/%m/%y"
    if request.method == 'POST':
        umbral_minimo = request.form['umbral_minimo']
        umbral_maximo = request.form['umbral_maximo']        
        if len(str(umbral_minimo))==0:
            umbral_minimo=0
        if len(str(umbral_maximo))==0:
            umbral_maximo=100
        archivo = open("./templates/home.html", "w")
        archivo.write('{% extends "numbers_layout.html" %}\n{% block numbers %}\n')
        from pymongo import MongoClient
        client = MongoClient()
        db = client.test
        cursor = db.numbers.find({"number": {"$gt": float(umbral_minimo), "$lt":float(umbral_maximo)}})
        for document in cursor:
            archivo.write("<tr><td>"+str(document["number"])+"</td><td>"+str(document["date"].strftime(formato_hora))+"</td><td>"+str(document["date"].strftime(formato_fecha))+"</td></tr>")
        archivo.write("\n{% endblock %}\n")
        archivo.write('{% block umbrales %}\n')
        archivo.write('<tr><td>La ultima vez que se genero un numero dentro de los umbrales marcados fue con fecha&nbsp;'+str(document["date"].strftime(formato_hora))+'&nbsp;'+str(document["date"].strftime(formato_fecha))+'con el numero&nbsp;'+str(document["number"])+'</td></tr>')
        archivo.write("\n{% endblock %}\n")
        archivo.close()
        return render_template('home.html')
    else:
        return 'El umbral es de hola'
@app.route('/about')
def about():
  return render_template('about.html')

  
if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
