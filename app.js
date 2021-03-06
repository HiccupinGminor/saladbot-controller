const express = require('express');
const app = express();
const PORT = 3000;
const bodyParser = require('body-parser');
const SerialPort = require('serialport');

const bodyRequired = function bodyRequired(req, res, next) {
	if(!req.body) {
		res.status(400);
		res.send({"error": "Must include body"});
	}
	else {
		next();
	}
};

app.use(bodyParser.json());

const port = new SerialPort('/dev/ttyACM0', { baudRate: 57600 });

// Open errors will be emitted as an error event
port.on('error', function(err) {
  console.log('Error: ', err.message);
})

// Switches the port into "flowing mode"
port.on('data', function (data) {
  console.log('Data:', Buffer.from(data, 'base64').toString());
});

app.post('/gcode', bodyRequired, function(req, res) {
	port.write(req.body.command + "\n", function(err) { // Force a newline
	  if (err) {
	    console.log("Error on write: ", err.message);
	    res.status(400);
	    res.send({"error": "Serial connection to mcu not established properly."});
	  }
	  else {
	  	res.status(200);
	  	res.send({"status": "OK"});	
	  }
	});
});

app.use(express.static('public'));

app.listen(PORT, function() {
	console.log(`App listening on port: ${ PORT }`)
});