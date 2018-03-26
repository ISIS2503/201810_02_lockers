from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

class Mock(Resource):
    def post(self):
        json_data = request.get_json(force = True)
        cuerpo = json_data['cuerpo']
        asunto = json_data['asunto']
        remitente = json_data['remitente']
        destinatario = ['destinatario']
        print('Se envió: '+cuerpo+' con asunto: '+asunto+' desde: '+remitente+' hacia: 'destinatario))

api.add_resource(Mock, '/mock')

if __name__ == '__main__':
    app.run(debug=True)
