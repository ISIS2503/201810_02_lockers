from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from pymongo import MongoClient
import datetime
import json

app = Flask(__name__)
api = Api(app)

clienteMongo = MongoClient('localhost', 27017)
db = clienteMongo['apirestfulencincominutos']
collection = db.alertas

class Alarmas(Resource):
    def get(self):
        x = {}
        cursor = collection.find({})
        i = 0
        for document in cursor:
            arreglo = []
            tipo = document['Tipo'].replace('\\', '')
            identificador = document['Identificador']
            informacion = document['Informacion'].replace('\\', '')
            hora = document['Hora']
            arreglo=[tipo, identificador, informacion, str(hora).replace('\\', '')]
            x['Alerta'+str(i)] = arreglo
            i+=1
        thejson = json.dumps([{k :{ 'Tipo':v[0], 'Identificador':v[1], 'Informacion': v[2], 'Hora': v[3]}} for k,v in x.items()])
        return thejson
    def post(self):
        json_data = request.get_json(force = True)
        tipo = json_data['Tipo']
        identificador = json_data['Identificador']
        informacion = json_data['Informacion']
        hora = datetime.datetime.utcnow()
        guardar = {
            'Tipo': tipo,
            'Identificador': identificador,
            'Informacion': informacion,
            'Hora': hora
            }
        collection.insert_one(guardar).inserted_id
        return jsonify(tipo = tipo, identificador = identificador, informacion = informacion, hora = hora)
               

api.add_resource(Alarmas, '/alarmas')

if __name__ == '__main__':
    app.run(debug=True, port = 5001)
    
