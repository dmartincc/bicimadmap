# -*- coding: utf-8 -*-
import requests, json, calendar, csv, feedparser
from datetime import datetime

time = datetime.now()
totalBikes = 1560
bikesOnTheGo = 0
bikesInStation = 0


def dateToMilliseconds(date):
	#parseDate=datetime.strptime(date, dt.timetuple())
	tupleDate=datetime.timetuple(date)               
	milliDate=calendar.timegm(tupleDate)*1000
	return milliDate

def writeCSV(data,nameFile):
	with open(nameFile+".csv", "wb") as file:
			csv_file = csv.writer(file)
			csv_file.writerow(data[0].keys())
			for item in data:
				csv_file.writerow(item.values())

def get_db(db_name):
    from pymongo import MongoClient
    uri = 'mongodb://user:passw0rd@kahana.mongohq.com:10070/bicimadmap'
    client = MongoClient(uri)
    db = client[db_name]
    return db  

def getData():
	db = get_db('bicimadmap')
	r = requests.get('http://bicimad.herokuapp.com/bicimad.json')
	d = feedparser.parse('http://weather.yahooapis.com/forecastrss?w=766273&u=c')	
	
	data=json.loads(r.text)	
	output=[]
	sumBikesOnStation = 0
	sumSpacesOnStation = 0
	for item in data[0]:
		dic={}
		dic['id']=item['numero_estacion']
		dic['name']=item['nombre'].encode('utf-8')		
		dic['datetime']=time
		dic['dateMilliseconds']=dateToMilliseconds(dic['datetime'])		
		dic['address']=item['direccion'].encode('utf-8')		
		dic['lat']=float(item['latitud'])
		dic['lng']=float(item['longitud'])
		dic['zone']= str(round(dic['lat'],2)) +"-"+ str(round(dic['lng'],2))
		if item['activo'] == "1":
			estado = True 
		else: 
			estado = False
		dic['active']= estado
		dic['bases']=int(item['numero_bases'])
		dic['free']=int(item['libres'])
		dic['bikes']=int(item['numero_bases'])-int(item['libres'])
		dic['disponibilityRate']=int(item['porcentaje'])		
		dic['occupyRate'] = 100-dic['disponibilityRate']	
		db.stations.insert(dic)
		#output.append(dic)

		sumBikesOnStation += dic['bikes']
		sumSpacesOnStation += dic['free']

	#Monitors the service's demand
	dic2 = {}
	dic2['datetime']=time
	dic2['dateMilliseconds']=dateToMilliseconds(dic2['datetime'])	
	dic2['occupyBikes']=totalBikes-sumBikesOnStation
	dic2['freeBikes']=sumBikesOnStation
	dic2['freeSpaces']=sumSpacesOnStation
	dic2['freeBikesRate']=(float(sumBikesOnStation)/totalBikes)*100
	dic2['occupyBikesRate'] = 100- dic2['freeBikesRate']
	dic2['windSpeed'] = float(d['feed']['yweather_wind']['speed'])
	dic2['temperature'] = int(d['feed']['yweather_wind']['chill'])
	dic2['pressure'] = float(d['feed']['yweather_atmosphere']['pressure'])
	dic2['humidity'] = float(d['feed']['yweather_atmosphere']['humidity'])
	dic2['visibility'] = float(d['feed']['yweather_atmosphere']['visibility'])
	dic2['weatherText'] = d['entries'][0]['yweather_condition']['text']
	dic2['weatherCode'] = int(d['entries'][0]['yweather_condition']['code'])
	 
	db.demand.insert(dic2)

	#it writes data just for one data and time
	#writeCSV(output,"data")


def extractData():
	db = get_db('bicimadmap')
	dataDemand = db.demand.find({"humidity":{"$ne":None}})
	output=[]
	for item in dataDemand:
		date=datetime.strptime(str(item['datetime']), "%Y-%m-%d %H:%M:%S.%f")
		item['weekday']= date.weekday()
		item['hour']= date.hour
		item['month']= date.month
		item['minute']= date.minute
		item['day']= date.day	
		output.append(item)

	writeCSV(output,"dataDemand")

	"""dataStations = db.stations.find()
	output=[]
	for item in dataStations:
		item['address']= item['address'].encode('utf-8')
		item['name']= item['name'].encode('utf-8')
		output.append(item)

	
	writeCSV(output,"dataStations")"""


def main():
	#getData()
	extractData()

if __name__ == '__main__':
	main()