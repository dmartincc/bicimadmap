from flask import render_template
from flask import jsonify
from app import app
import json, time, requests

@app.route('/')
def index():
    
    r = requests.get('http://bicimad.herokuapp.com/bicimad.json')
    data=json.loads(r.text)
    dataNew=[]
    geo=[]
    for item in data[0]:
		dic={}
		dic['name']=item['nombre']
		dic['adress']=item['direccion']
		dic['lat']=float(item['latitud'])
		dic['lng']=float(item['longitud'])
		if item['activo'] == "1": 
			estado = "Activo" 
		else: 
			estado = "No Activo"
		dic['active']= estado
		dic['bases']=int(item['numero_bases'])
		dic['free']=int(item['libres'])
		dic['bikes']=int(item['numero_bases'])-int(item['libres'])
		dic['availability']=item['porcentaje']
		dataNew.append(dic)
     
    
    return render_template("index.html", data = dataNew)


@app.route('/about')
def about():
	return render_template("about.html")

       


    

