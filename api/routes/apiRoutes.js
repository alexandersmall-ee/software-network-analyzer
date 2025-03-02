// api routing file

// import express to create a router
// initialize router instance
const express = require('express');
const router = express.Router();

// test signal route
// define test signal api endpoint 
router.get('/test-signal', (req, res) => {
    res.json({ message: 'Test signal sent to oscilloscope' });
});

// define measurements api endpoint 
router.get('/measurements', (req, res) => {
    res.json({ amplitude: 3.2, phase: 45.5 });
});

// export the router so it can be used in the main server file
module.exports = router;
