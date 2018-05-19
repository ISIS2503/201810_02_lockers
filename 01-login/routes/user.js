const express = require('express');
const passport = require('passport');
const ensureLoggedIn = require('connect-ensure-login').ensureLoggedIn();
const router = express.Router();
const https = require('http');

/* GET user profile. */
router.get('/inmuebles/:inmue/:inmu', ensureLoggedIn, function(req, res, next) {
  let inm='';
  if(req.user._json['https://lockers/roles'][0]==="administrador"){
    res.render('user', {
      user: req.user
    }); 
  }
  else if(req.user._json['https://lockers/roles'][0]==="seguridad"){
    var postData = JSON.parse('{"dondeUnidad":0,"dondeInmueble":'+req.params.inmue+',"numeroApto":'+req.params.inmu+'}');
    var options = {
      host: '172.24.42.82',
      port: 8083,
      method:'POST',
      path:'/inmueblesGet',
      headers: {
        'Content-Type': 'application/json'      }
    };
    var req2=https.request(options,(resp) => {
      let data = '';
      // A chunk of data has been recieved.
      resp.on('data', (chunk) => {
        data = chunk;
        inm =JSON.parse(data);
        //inm=data;
        res.render('inmuebleDetail', {
          inmueble: inm,
          tipo:'sin'
        });
        
      });   
    }).on("error", (err) => {
      console.log("Error: " + err.message);
    });
    req2.write(JSON.stringify(postData));
    console.log(inm);
    req2.end();
    options = {
      host: '172.24.42.82',
      port: 8083,
      method:'POST',
      path:'/cambiar',
      headers: {
        'Content-Type': 'application/json'      }
    };
    var req3=https.request(options,(resp) => {
      let data = '';
      // A chunk of data has been recieved.
      resp.on('data', (chunk) => {
        data = chunk;
        inm =JSON.parse(data);
      });   
    }).on("error", (err) => {
      console.log("Error: " + err.message);
    });
    req3.write(JSON.stringify(postData));
    req3.end();
  }
  else{
    res.render('propietario', {
      user: req.user
    }); 
  }
});

router.get('/', ensureLoggedIn, function(req, res, next) {
  if(req.user._json['https://lockers/roles'][0]==="administrador"){
    res.render('user', {
      user: req.user
    }); 
  }
  else if(req.user._json['https://lockers/roles'][0]==="seguridad"){
    var inm ={};
    var body='';
    https.get('http://172.24.42.82:8083/seguridad/'+req.user.nickname,(resp) => {
      resp.on('data', function(chunk){
        body += chunk;
      });
      resp.on('end',function(){
        inm = JSON.parse(body);
        res.render('security', {
          inmuebles: inm,
          href: '/user'
        }); 
      });
    }).on("error", (err) => {
      console.log("Error: " + err.message);
    });
    
  }
  else{
    res.render('propietario', {
      user: req.user
    }); 
  }
});

router.get('/alarma', ensureLoggedIn, function(req, res, next) {
  if(req.user._json['https://lockers/roles'][0]==="administrador"){
    res.render('user', {
      user: req.user
    }); 
  }
  else if(req.user._json['https://lockers/roles'][0]==="seguridad"){
    var inm ={};
    var body='';
    https.get('http://172.24.42.82:8083/seguridad/'+req.user.nickname,(resp) => {
      resp.on('data', function(chunk){
        body += chunk;
      });
      resp.on('end',function(){
        inm = JSON.parse(body);
        for(var i = 0; i<inm[0].unidades[0].inmuebles.length;i++){
            var alerts = inm[0].unidades[0].inmuebles[i].hubs[0].alarmas;
            var goodAlerts =[];
            for(var y=0 ; y< alerts.length;y++){
              if(alerts[y].tipo==="alarma"){
                goodAlerts.push(alerts[y]);
              }
            }
            inm[0].unidades[0].inmuebles[i].hubs[0].alarmas=goodAlerts;
        }
        res.render('security', {
          inmuebles: inm,
          href: '/user/alarma'
        }); 
      });
    }).on("error", (err) => {
      console.log("Error: " + err.message);
    });
    
  }
  else{
    res.render('propietario', {
      user: req.user
    }); 
  }
});

router.get('/fallo', ensureLoggedIn, function(req, res, next) {
  if(req.user._json['https://lockers/roles'][0]==="administrador"){
    res.render('user', {
      user: req.user
    }); 
  }
  else if(req.user._json['https://lockers/roles'][0]==="seguridad"){
    var inm ={};
    var body='';
    https.get('http://172.24.42.82:8083/seguridad/'+req.user.nickname,(resp) => {
      resp.on('data', function(chunk){
        body += chunk;
      });
      resp.on('end',function(){
        inm = JSON.parse(body);
        for(var i = 0; i<inm[0].unidades[0].inmuebles.length;i++){
            var alerts = inm[0].unidades[0].inmuebles[i].hubs[0].alarmas;
            var goodAlerts =[];
            for(var y=0 ; y< alerts.length;y++){
              if(alerts[y].tipo==="fallo"){
                goodAlerts.push(alerts[y]);
              }
            }
            inm[0].unidades[0].inmuebles[i].hubs[0].alarmas=goodAlerts;
        }
        res.render('security', {
          inmuebles: inm,
          href: '/user/fallo'
        }); 
      });
    }).on("error", (err) => {
      console.log("Error: " + err.message);
    });
    
  }
  else{
    res.render('propietario', {
      user: req.user
    }); 
  }
});

router.get('/:tipo/inmuebles/:inmue/:inmu', ensureLoggedIn, function(req, res, next) {
  let inm='';
  if(req.user._json['https://lockers/roles'][0]==="administrador"){
    res.render('user', {
      user: req.user
    }); 
  }
  else if(req.user._json['https://lockers/roles'][0]==="seguridad"){
    var postData = JSON.parse('{"dondeUnidad":0,"dondeInmueble":'+req.params.inmue+',"numeroApto":'+req.params.inmu+',"tipo":"'+req.params.tipo+'"}');
    var options = {
      host: '172.24.42.82',
      port: 8083,
      method:'POST',
      path:'/inmueblesGetTipo',
      headers: {
        'Content-Type': 'application/json'      }
    };
    var req2=https.request(options,(resp) => {
      let data = '';
      // A chunk of data has been recieved.
      resp.on('data', (chunk) => {
        data = chunk;
        inm =JSON.parse(data);
        //inm=data;
        res.render('inmuebleDetail', {
          inmueble: inm, 
          tipo : req.params.tipo
        });
        
      });   
    }).on("error", (err) => {
      console.log("Error: " + err.message);
    });
    req2.write(JSON.stringify(postData));
    console.log(inm);
    req2.end();
    options = {
      host: '172.24.42.82',
      port: 8083,
      method:'POST',
      path:'/cambiar',
      headers: {
        'Content-Type': 'application/json'      }
    };
    var req3=https.request(options,(resp) => {
      let data = '';
      // A chunk of data has been recieved.
      resp.on('data', (chunk) => {
        data = chunk;
        inm =JSON.parse(data);
      });   
    }).on("error", (err) => {
      console.log("Error: " + err.message);
    });
    req3.write(JSON.stringify(postData));
    req3.end();
  }
  else{
    res.render('propietario', {
      user: req.user
    }); 
  }
});

module.exports = router;
