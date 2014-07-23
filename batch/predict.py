import PyPredictor as pp

values = {}
values['hour'] = 8
values['humidity'] = 90
values['weatherCode'] = 34
values['day'] = 12
values['weekday'] = 0
values['temperature'] = 20
values['windSpeed'] = 2
values['minute'] = 30
values['pressure'] = 1080

prediction=pp.predict('bicimadmapPredictionModel.pmml', values)
print prediction