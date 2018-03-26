var mongoose = require('mongoose');

var AlarmaSchema = mongoose.Schema({
  name: String,
  codigo: String,
  date: String,
  descripcion: String
});


module.exports = mongoose.model('Alarma', AlarmaSchema);
