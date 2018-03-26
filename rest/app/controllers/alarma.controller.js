var Alarma = require('../models/alarma.model.js');

exports.todos = function(req, res) {
  Alarma.find(function(err, alarmas){
      if(err) {
          console.log(err);
          res.status(500).send({message: "Some error occurred while retrieving notes."});
      } else {
          res.send(alarmas);
      }
  });
};
