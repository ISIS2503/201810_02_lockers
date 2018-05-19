const express = require('express');
const app = express();
const mongoose = require('mongoose');

var bodyParser = require('body-parser')
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));

app.use(express.json());
app.use(express.urlencoded());

var Schema = mongoose.Schema;
mongoose.set('debug', true);
mongoose.connect('mongodb://localhost/arquisoft');

var estado = false;

var passSchema = new Schema({index: Number, value: Number}, {collection: 'usuarios'});

var alarmSchema = new Schema({id: Number, tipo: String, informacion: String, timeStamp: Date, visto:Boolean}, {collection: 'usuarios'})

var cerraduraSchema = new Schema({
  id: Number,
  passwords: [
    {
      type: Schema.Types.Mixed,
      ref: 'Pass'
    }
  ]
}, {collection: 'usuarios'});

var alarmasSchema = new Schema({
  alarmas: [
    {
      type: Schema.Types.Mixed,
      ref: 'Alarma'
    }
  ]
}, {collection: 'usuarios'})

var propietarioSchema = new Schema({nombre: String, email: String, telefono: Number}, {collection: 'usuarios'})

var hubSchema = new Schema({
  cerradura: [
    {
      type: Schema.Types.Mixed,
      ref: 'Cerradura'
    }
  ],
  alarmas: [
    {
      type: Schema.Types.Mixed,
      ref: 'Alarma'
    }
  ],
  propietario: [
    {
      type: Schema.Types.Mixed,
      ref: 'Propietario'
    }
  ],
  numeroApto: Number
}, {collection: 'usuarios'})

var inmuebleSchema = new Schema({
  hubs: [
    {
      type: Schema.Types.Mixed,
      ref: 'Hub'
    }
  ],
  id: Number,
  nombre: String,
  barrio: String
}, {collection: 'usuarios'})

var unidadSchema = new Schema({
  _id: Schema.Types.ObjectId,
  inmuebles: [
    {
      type: Schema.Types.Mixed,
      ref: 'Inmueble'
    }
  ]
}, {collection: 'usuarios'})

var unidadesSchema = new Schema({
  _id: Schema.Types.ObjectId,
  unidades: [
    {
      type: Schema.Types.Mixed,
      ref: 'Unidad'
    }
  ]
}, {collection: 'usuarios'})

var Pass = mongoose.model('passwords', passSchema);
var Alarma = mongoose.model('alarmas', alarmSchema);
var Cerradura = mongoose.model('cerradura', cerraduraSchema);
var Propietario = mongoose.model('propietario', propietarioSchema);
var Hub = mongoose.model('hubs', hubSchema);
var Inmueble = mongoose.model('inmuebles', inmuebleSchema);
var Unidad = mongoose.model('unidades', unidadSchema);
var Yale = mongoose.model('usuarios', unidadesSchema);

app.get('/', function(req, res) {
  Yale.find({}).exec(function(err, unidades) {
    if (err)
      throw err;
    res.json(unidades);
  });
})

app.get('/seguridad/:usuario', function(req, res) {
  var paramDs = {}
  paramDs["unidades.seguridad"] = req.params.usuario;
  Yale.find(paramDs).exec(function(err, unidades) {
    if (err)
      throw err;
    res.json(unidades);
  });
})




app.post('/alarmasInmueble', function(req, res) {
  var dondeUnidad = req.body.dondeUnidad;
  var dondeInmueble = req.body.dondeInmueble;
  var numeroApto = req.body.numeroApto;
  var parametro = "unidades."+dondeUnidad+".inmuebles."+dondeInmueble+".hubs.numeroApto";
  var parametroD = "unidades."+dondeUnidad+".inmuebles."+dondeInmueble+".hubs.alarmas";
  var paramDs = {}
  paramDs[parametro] = numeroApto;
  var paramO = {};
  paramO["unidades.0.inmuebles.1.hubs.alarmas"] = 1;
  Yale.findOne(paramDs, 'unidades.inmuebles.hubs.alarmas').exec(function(err, unidades) {
    if (err)
      throw err;
    try
    {
      res.json(unidades.unidades[dondeUnidad].inmuebles[dondeInmueble].hubs);
    }
    catch(error){
      res.json('No se encuentra');
    }

  });
})

app.post('/inmueblesGet', function(req, res) {
  var dondeUnidad = req.body.dondeUnidad;
  var dondeInmueble = req.body.dondeInmueble;
  var numeroApto = req.body.numeroApto;
  var parametro = "unidades."+dondeUnidad+".inmuebles."+dondeInmueble+".hubs.numeroApto";
  var paramDs = {}
  paramDs[parametro] = numeroApto;
  Yale.findOne(paramDs, 'unidades.inmuebles.hubs').exec(function(err, unidades) {
    if (err)
      throw err;
    try
    {

      res.json(unidades.unidades[dondeUnidad].inmuebles[dondeInmueble].hubs);
    }
    catch(error){
      res.json('No se encuentra');
    }

  });
})

app.post('/inmueblesGetTipo', function(req, res) {
  var dondeUnidad = req.body.dondeUnidad;
  var dondeInmueble = req.body.dondeInmueble;
  var numeroApto = req.body.numeroApto;
  var tipo = req.body.tipo;
  var parametro = "unidades."+dondeUnidad+".inmuebles."+dondeInmueble+".hubs.numeroApto";
  var parametroTipo = "unidades."+dondeUnidad+".inmuebles."+dondeInmueble+".hubs.0.alarmas.tipo";
  var paramDs = {}
  paramDs[parametro] = numeroApto;
  var paramTipo = {}
  paramTipo[parametroTipo] = tipo;
  var paramSelector = {};
  paramSelector["unidades.inmuebles.hubs.alarmas.tipo"] = tipo;
  Yale.findOne({'$and': [paramDs, paramTipo] }, 'unidades.inmuebles.hubs').exec(function(err, unidades) {
    if (err)
      throw err;
    try
    {
      var jsonT = [];
      var jsonU ={};
      var jsonK = unidades.unidades[dondeUnidad].inmuebles[dondeInmueble].hubs[0];
      var jsonC = unidades.unidades[dondeUnidad].inmuebles[dondeInmueble].hubs[0].alarmas;
      var jsonF = [];
      for(var i  in jsonC){
        if(jsonC[i].tipo===tipo){
          jsonF.push(jsonC[i]);
        }
      }
      var cerradura = {};
      cerradura["cerradura"] = jsonK.cerradura;
      var numeroApto = {};
      numeroApto["numeroApto"] = jsonK.numeroApto;
      jsonU['cerradura']=(cerradura);
      jsonU['propietario']=(jsonK.propietario);
      jsonU['numeroApto']=(numeroApto);
      jsonU['alarmas']=(jsonF);
      jsonT.push(jsonU)
      res.json(jsonT);
    }
    catch(error){
      res.json(error.message);
    }

  });
})

app.post('/cambiar', function(req, res) {
  var dondeUnidad = req.body.dondeUnidad;
  var dondeInmueble = req.body.dondeInmueble;
  var numeroApto = req.body.numeroApto;
  var parametro = "unidades."+dondeUnidad+".inmuebles."+dondeInmueble+".hubs.numeroApto";
  var parametroo = "unidades."+dondeUnidad+".inmuebles."+dondeInmueble+".hubs.0.alarmas.$[].visto";
  var paramValor = "true";
  var paramDs = {}
  paramDs[parametro] = numeroApto;
  var paramm = {}
  paramm[parametroo] = paramValor;
  Yale.update(paramDs, {'$set': paramm}).exec(function(err, unidades) {
    if (err)
      throw err;
    try
    {
      res.json(unidades);
    }
    catch(error){
      res.json('No se encuentra');
    }

  });
})

app.post('/', function(req, res) {
  var que = req.body.que;
  if (que === 'Usuario') {
    var dondeHub = req.body.dondeHub;
    var dondeInmueble = req.body.dondeInmueble;
    var dondeUnidad = req.body.dondeUnidad;
    var numeroApto = req.body.numeroApto;
    var propietario = req.body.propietario;
    var nombre = propietario.nombre;
    var email = propietario.email;
    var telefono = propietario.telefono;
    var donde = 'unidades.'+dondeUnidad+'.inmuebles.'+dondeInmueble+'.id';
    var dondeConHub = 'unidades.'+dondeUnidad+'.inmuebles';
    var hubs = [{
      cerradura:[{}],
      alarmas: [{
          "id" : 0,
          "tipo" : "alarma",
          "informacion" : "Primera Alarma",
          "timeStamp" : Date.now(),
          "visto" : "false"
      }],
      propietario:[{
        nombre: nombre,
        email: email,
        telefono: telefono
      }],
      numeroApto: numeroApto
    }];
    var hubA = [{hubs}];
    var queryParam = {};
    queryParam[donde] = dondeInmueble;
    var paramD = {};
    paramD[dondeConHub] = hubA;
    Yale.update(queryParam, {$push: paramD}).exec(function(err, unidades) {
      if (err)
        throw err;
      res.json(unidades);
    });
  }
});

app.post('/alarmas', function(req, res) {
  var que = req.body.que;
  if (que === 'Alarma') {
    var dondeHub = req.body.dondeHub;
    var dondeInmueble = req.body.dondeInmueble;
    var dondeUnidad = req.body.dondeUnidad;
    var numeroApto = parseInt(req.body.numeroApto);
    var id = req.body.id;
    var tipo = req.body.tipo;
    var timeStamp = Date.now();
    var visto = false;
    var informacion = req.body.informacion;
    var donde = 'unidades.'+dondeUnidad+'.inmuebles.'+dondeInmueble+'.hubs.'+dondeHub+'.alarmas';
    var dondeConHub = 'unidades.'+dondeUnidad+'.inmuebles.'+dondeInmueble+'.hubs.'+dondeHub+'.numeroApto';
    var alarmaF = {
      id:id,
      tipo: tipo,
      informacion: informacion,
      timeStamp: timeStamp,
      visto : visto
    };
    var queryParam = {};
    queryParam[dondeConHub] = numeroApto;
    var paramD = {};
    paramD[donde] = alarmaF;
    Yale.update(queryParam, {$push: paramD}).exec(function(err, unidades) {
      if (err)
        throw err;
      res.json(unidades);
      cambiarEstadoTrue();
    });
  }
});

app.get('/estado', function(req, res){
  var jsoni = {"estado": estado};
  res.json(jsoni);
})

app.get('/cambiarEstado', function(req, res){
  cambiarEstadoFalse();
  var cambio = {"cambio": "false"};
  res.json(cambio);
});

function cambiarEstadoTrue() {
  estado = true;
}

function cambiarEstadoFalse() {
  estado = false;
}

app.listen(8083, function() {
  console.log('Listening on 8083')
})
