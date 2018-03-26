module.exports = function(app) {

    var alarmas = require('../controllers/alarma.controller.js');

    // Retrieve all Notes
    app.get('/alarmas', alarmas.todos);
}
