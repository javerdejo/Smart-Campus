var express = require("express"),
   app = express(),
   bodyParser = require("body-parser"),
   methodOverride = require("method-override");

var mysql = require('mysql'),
   connection = mysql.createConnection({
      host: 'localhost',
      user: 'root',
      password: 'patolucas',
      database: 'umacamp'
   });

app.use(bodyParser.urlencoded({
   extended: false
}));
app.use(bodyParser.json());
app.use(methodOverride());

var router = express.Router();

router.post('/add/sound/', function(req, res) {
   res.status(200);
   res.end();

   if (connection) {
      connection.query(
         `insert into sound (sensor_id, noise, peak, date_time) values (${req.body.sensor_id},${req.body.noise},${req.body.peak},'${req.body.date_time}')`,
         function(
            error, result) {
            if (error) {
               throw error;
            } else {
               //console.log("- saound data added on " + Date());
            }
         });
   }
});

router.post('/add/wifi/', function(req, res) {
   res.status(200);
   res.end();

   if (connection) {
      connection.query(
         `insert into wifi (sensor_id, mac_address, first_time, last_time) values (${req.body.sensor_id},'${req.body.mac_address}','${req.body.first_time}','${req.body.last_time}')`,
         function(
            error, result) {
            if (error) {
               throw error;
            } else {
               //console.log("- wifi data added on " + Date());
            }
         });
   }
});

router.post('/add/bluetooth/', function(req, res) {
   res.status(200);
   res.end();

   if (connection) {
      connection.query(
         `insert into bluetooth (sensor_id, mac_address, duration, date_time) values (${req.body.sensor_id},'${req.body.mac_address}',${req.body.duration},'${req.body.date_time}')`,
         function(
            error, result) {
            if (error) {
               throw error;
            } else {
               //console.log("- bluetooth data added on " + Date());
            }
         });
   }
});

app.use(router);

app.listen(3000, function() {
   console.log("Node UMACamp server running on http://localhost:3000");
});