// main server file

// define configurable settings
require('dotenv').config();
// import express
const express = require('express');
// cors allows requests from different origins 
// useful, here, for when the frontend makes calls to the api 
const cors = require('cors');

// initialize an express app
const app = express();
// define port number
const PORT = process.env.PORT || 5005;
//import api routes
const apiRoutes = require('./routes/apiRoutes');

// mount api routes under api directory
// enable cors and json parser for requests 
app.use('/api', apiRoutes);
app.use(cors());
app.use(express.json()); // Body parser is built into Express now

app.get('/', (req, res) => {
    res.send('Network Analyzer API is running...');
});

// start the server and listen for incoming requests on the port
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
