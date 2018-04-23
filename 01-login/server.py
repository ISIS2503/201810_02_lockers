"""Python Flask WebApp Auth0 integration example
"""
from functools import wraps
import json
from os import environ as env
from werkzeug.exceptions import HTTPException

from dotenv import load_dotenv, find_dotenv
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for, redirect, request
from authlib.flask.client import OAuth
from six.moves.urllib.parse import urlencode
from pymongo import MongoClient
import paho.mqtt.client as mqtt
import requests
import datetime

import constants

def on_connect(client, userdata, flags, rc):
    app.logger.info("Connected with result code "+str(rc))

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

AUTH0_CALLBACK_URL = env.get(constants.AUTH0_CALLBACK_URL)
AUTH0_CLIENT_ID = env.get(constants.AUTH0_CLIENT_ID)
AUTH0_CLIENT_SECRET = env.get(constants.AUTH0_CLIENT_SECRET)
AUTH0_DOMAIN = env.get(constants.AUTH0_DOMAIN)
AUTH0_BASE_URL = 'https://' + AUTH0_DOMAIN
AUTH0_AUDIENCE = env.get(constants.AUTH0_AUDIENCE)
if AUTH0_AUDIENCE is '':
    AUTH0_AUDIENCE = AUTH0_BASE_URL + '/userinfo'

app = Flask(__name__, static_url_path='/public', static_folder='./public')
app.secret_key = constants.SECRET_KEY
app.debug = True

clienteMongo = MongoClient('localhost', 27017)
db = clienteMongo['claves']
collection = db.clavesistema

client = mqtt.Client();
client.on_connect=on_connect;
client.connect("172.24.42.82",8083,60);


@app.errorhandler(Exception)
def handle_auth_error(ex):
    response = jsonify(message=str(ex))
    response.status_code = (ex.code if isinstance(ex, HTTPException) else 500)
    return response


oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    api_base_url=AUTH0_BASE_URL,
    access_token_url=AUTH0_BASE_URL + '/oauth/token',
    authorize_url=AUTH0_BASE_URL + '/authorize',
    client_kwargs={
        'scope': 'openid profile',
    },
)


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if constants.PROFILE_KEY not in session:
            return redirect('/login')
        return f(*args, **kwargs)

    return decorated


# Controllers API
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/callback')
def callback_handling():
    resp = auth0.authorize_access_token()

    url = AUTH0_BASE_URL + '/userinfo'
    headers = {'authorization': 'Bearer ' + resp['access_token']}
    resp = requests.get(url, headers=headers)
    userinfo = resp.json()

    session[constants.JWT_PAYLOAD] = userinfo

    session[constants.PROFILE_KEY] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }

    return redirect('/dashboard')


@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL, audience=AUTH0_AUDIENCE)


@app.route('/logout')
def logout():
    session.clear()
    #params = {'returnTo': url_for('home', _external=True), 'client_id': AUTH0_CLIENT_ID}
    return login()


@app.route('/dashboard')
@requires_auth
def dashboard():
    client = mqtt.Client();
    client.on_connect=on_connect;
    client.connect("172.24.42.82",8083,60);
    app.logger.info(session['jwt_payload']['http://lockers/roles'])
    return render_template('dashboard.html',
                           userinfo=session[constants.PROFILE_KEY],
                           userinfo_pretty=json.dumps(session[constants.JWT_PAYLOAD], indent=4))

@app.route('/todo')
@requires_auth
def eliminarTodo():
    client = mqtt.Client();
    client.on_connect=on_connect;
    client.connect("172.24.42.82",8083,60);
    try:
        rol = session['jwt_payload']['http://lockers/roles'][0]
        if(rol=='yale'):
            collection.remove({})
            client.publish("claves/", "DELETE_ALL_PASSWORDS;")
            return ("Se eliminaron todas las claves")
        else:
            return ("No se cuentan con los suficientes permisos")
    except Exception as e:
        return ("Ocurrio un problema: "+str(e))

def eliminarEspecifico(passw):
    client = mqtt.Client();
    client.on_connect=on_connect;
    client.connect("172.24.42.82",8083,60);
    try:
        if(collection.find({"clave" : passw}).count()==1):
            indice = db.clavesistema.find({"clave": passw}, { "indice": 1})[0]['indice']
            app.logger.info(str(indice))
            db.clavesistema.remove({"clave": passw})
            stringArmada = "DELETE_PASSWORD;"+str(indice)+";"
            client.publish("claves/", stringArmada)
            return ("Se elimino la clave")
        else:
            return("No existe dicha clave")
    except Exception as e:
        return ("Ocurrio un problema: "+str(e))
    
@app.route('/especifica', methods = ['POST'])
@requires_auth
def eliminarUno():
    try:
        tiempo = datetime.datetime.now()
        lascinco = tiempo.replace(hour=5, minute=0, second=0, microsecond=0)
        lasonce = tiempo.replace(hour=23, minute=0, second=0, microsecond=0)
        passw = request.form['clave']
        indice = request.form['index']
        rol = session['jwt_payload']['http://lockers/roles'][0]
        app.logger.info(rol)
        if((rol == 'administrador') & (int(indice) <=15)):
            return(eliminarEspecifico(passw))
        elif((rol == 'seguridad') & (int(indice) <=10)):
            return(eliminarEspecifico(passw))
        elif((rol == 'propietario') & (int(indice) <=5)):
            if((tiempo>lascinco) & (tiempo<lasonce)):
                return(eliminarEspecifico(passw))
            else:
                return("Hora no permitida")
        elif((rol == 'yale') & (int(indice) <=20)):
            return(eliminarEspecifico(passw))
        else:
            return("Operacion no permitida para este rol. Verifique el indice")
    except Exception as e:
        return ("Ocurrio un problema: "+str(e))      

def crearPass(index, passw):
    client = mqtt.Client();
    client.on_connect=on_connect;
    client.connect("172.24.42.82",8083,60);
    try:
        if(len(passw)==4):
            if(passw.isnumeric()):
                if(collection.count()<20):
                    if(collection.find({"clave" : passw}).count()==0):
                        app.logger.info(collection.find({"clave" : passw}).count())
                        collection.insert_one({"clave": passw, "indice": index}).inserted_id
                        stringArmada = "CREATE_PASSWORD;"+str(index)+";"+str(passw)+";"
                        client.publish("claves/", stringArmada)
                        return ("Se creo la clave de manera exitosa.")
                    else:
                        return ("Ya hay una clave igual")
                else:
                    return ("Se llegó a un máximo de claves")
            else:
                return ("La clave debe ser totalmente numerica")
        else:
            return ("La clave tiene un tamaño no permitido. Debe ser de 4")
    except Exception as e:
        return ("Ocurrio un problema: "+str(e))
    
@app.route('/crear', methods = ['POST'])
@requires_auth
def crear():
    try:
        tiempo = datetime.datetime.now()
        lascinco = tiempo.replace(hour=5, minute=0, second=0, microsecond=0)
        lasonce = tiempo.replace(hour=23, minute=0, second=0, microsecond=0)
        passw = request.form['clave']
        indice = request.form['index']
        rol = session['jwt_payload']['http://lockers/roles'][0]
        app.logger.info(rol)
        if((rol == 'administrador') & (int(indice) <=15)):
            return(crearPass(indice, passw))
        elif((rol == 'seguridad') & (int(indice) <=10)):
            return(crearPass(indice, passw))
        elif((rol == 'propietario') & (int(indice)<=5)):
            if((tiempo>lascinco) & (tiempo<lasonce)):
                return(crearPass(indice, passw))
            else:
                return("Hora no permitida")
        elif((rol == 'yale') & (int(indice) <=20) ):
            return(crearPass(indice, passw))
        else:
            return("Operacion no permitida para este rol. Verifique el indice")
    except Exception as e:
        return ("Ocurrio un problema: "+str(e))        

def actualizarUno(indice, passw, passwN):
    client = mqtt.Client();
    client.on_connect=on_connect;
    client.connect("172.24.42.82",8083,60);
    try:
        if(collection.find({"clave" : passw}).count()==1):
            db.clavesistema.update_one({"clave":passw}, {"$set": {"clave": passwN}})
            stringArmada = "UPDATE_PASSWORD;"+str(indice)+";"+str(passwN)+";"
            client.publish("claves/", stringArmada)
            return ("Se actualizo la clave")
        else:
            return("No existe dicha clave")
    except Exception as e:
        return ("Ocurrio un problema: "+str(e))

@app.route('/actualizarUna', methods = ['POST'])
@requires_auth
def actualizar():
    try:
        tiempo = datetime.datetime.now()
        lascinco = tiempo.replace(hour=5, minute=0, second=0, microsecond=0)
        lasonce = tiempo.replace(hour=23, minute=0, second=0, microsecond=0)
        passw = request.form['claveAntigua']
        passwN = request.form['claveNueva']
        indice = request.form['index']
        rol = session['jwt_payload']['http://lockers/roles'][0]
        if((rol == 'administrador') & (int(indice) <=15) & (int(indice)>=11)):
            return(actualizarUno(indice, passw, passwN))
        elif((rol == 'seguridad') & (int(indice) <=10) & (int(indice)>=6)):
            return(actualizarUno(indice, passw, passwN))
        elif((rol == 'propietario') & (int(indice)>=1) & (int(indice) <=5)):
            if((tiempo>lascinco) & (tiempo<lasonce)):
                return(actualizarUno(indice, passw, passwN))
            else:
                return("Hora no permitida")
        elif((rol == 'yale') & (int(indice) <=20) & (int(indice)>=16) ):
            return(actualizarUno(indice, passw, passwN))
        else:
            return("Operacion no permitida para este rol. Verifique el indice")
    except Exception as e:
        return ("Ocurrio un problema: "+str(e))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=env.get('PORT', 3000))
