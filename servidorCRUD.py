from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from pymongo import MongoClient
import datetime
import json
import os

app = Flask(__name__)
api = Api(app)

clienteMongo = MongoClient('localhost', 27017)
db = clienteMongo['apirestfulencincominutos']
collection = db.sistema

class Sistemas(Resource):
    def get(self):
        a = ''
        cursor = collection.find({})
        for document in cursor:
            a += str(document)+', '
        return str(a)[0:len(a)-2]
    def post(self):
        json_data = request.get_json(force = True)
        devolver = jsonify(json_data)
        collection.insert_one(json_data).inserted_id
        return devolver
    def delete(self):
        json_data = request.get_json(force = True)
        cambio = json_data['cambio']
        iden = json_data['id']
        if(cambio == 'unidad'):
            collection.delete_many({"unidadResidencial.id_unidad": iden})
        elif(cambio == 'inmueble'):
            collection.delete_many({"inmuble.id_inmueble": iden})
        elif(cambio == 'hub'):
            collection.delete_many({"hub.id_hub": iden})
        elif(cambio == 'cerradura'):
            collection.delete_many({"cerradura.id_cerradura": iden})
        return jsonify(json_data)
    def put(self):
        json_data = request.get_json(force = True)
        cambio = json_data['cambio']
        iden = json_data['id_viejo']
        idenuevo = json_data['id_nuevo']
        if(cambio == 'unidad'):
            collection.update_one({"unidad.id_unidad": iden}, {"$set": {"unidad.id_unidad": idenuevo} })
        elif(cambio == 'inmueble'):
            collection.update_one({"inmueble.id_inmueble": iden}, {"$set": {"inmueble.id_inmueble": idenuevo} })
        elif(cambio == 'hub'):
            collection.update_one({"hub.id_inmueble": iden}, {"$set": {"hub.id_hub": idenuevo} })
        elif(cambio == 'cerradura'):
            collection.update_one({"cerradura.id_cerradura": iden}, {"$set": {"cerradura.id_cerradura": idenuevo} })
        return jsonify(json_data)

api.add_resource(Sistemas, '/sistemas')

if __name__ == '__main__':
    app.run(debug=True)
