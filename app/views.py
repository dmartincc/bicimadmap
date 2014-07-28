from flask import render_template, request, jsonify
from app import app
import json, time, requests
from functions import *


@app.route('/')
def index(): 
	r = requests.get('http://bicimad-api.herokuapp.com/api-v1/locations')   
	data=json.loads(r.text)
	db = get_db('bicimadmap')  
	dataNew=[]
	geo=[]
	for item in data['locations']:
		dic={}
		data=db.stations.find({'id':item['idestacion']}).limit(1)
		dic['name']=item['nombre']
		dic['adress']=item['direccion']
		dic['lat']=float(item['latitud'])
		dic['lng']=float(item['longitud'])
		if item['activo'] == True: 
			estado = "Activo" 
		else: 
			estado = "No Activo"
		dic['active']= estado
		dic['bases']=data[0]['bases']
		dic['free']=int(item['libres'])
		dic['bikes']=dic['bases']-int(item['libres'])
		dic['availability']=item['porcentaje']
		dataNew.append(dic)
	 

	return render_template("index.html", data = dataNew, title="Bienvenido")


@app.route('/about')
def about():
	return render_template("about.html", title="Sobre BiciMadMap")

@app.route('/analytics')
def analytics():
	db = get_db('bicimadmap')
	data=db.demand.find().sort("datetime",-1).limit(1)
	perc=int(data[0]['occupyBikesRate'])

	dataAll=db.demand.find()
	if request.args.get('query') :
		if request.args.get('query') == "free":
			timeSerie=[{"key":"Bicicletas Libres","values":[]}]
			for item in dataAll:		
				timeSerie[0]['values'].append([item['dateMilliseconds'],item['freeBikes']])
		elif request.args.get('query') == "occupy":
			timeSerie=[{"key":"Bicicletas Ocupadas","values":[]}]
			for item in dataAll:		
				timeSerie[0]['values'].append([item['dateMilliseconds'],item['occupyBikes']])		
		elif request.args.get('query') == "rate":
			timeSerie=[{"key":"Tasa de ocupacion","values":[]}]
			for item in dataAll:
				timeSerie[0]['values'].append([item['dateMilliseconds'],item['occupyBikesRate']])
	else:
		timeSerie=[{"key":"Bicicletas Ocupadas","values":[]}]
		for item in dataAll:		
			timeSerie[0]['values'].append([item['dateMilliseconds'],item['occupyBikes']])

	return render_template("analytics.html", 
							title="BiciMadMap Analytics", 
							data=data,
							perc=perc,
							timeSerie=timeSerie,
							graph=True)

@app.route('/sitemap')
def sitemap():
    url_root = request.url_root[:-1]
    rules = app.url_map.iter_rules()
    return render_template('sitemap.xml', url_root=url_root, rules=rules)

       


    

