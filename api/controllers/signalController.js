/**
 * Sends a test signal command to the oscilloscope.
 * This function calls the Python script and passes frequency/waveform arguments.
 * 
 * Design Decision:
 * - Using `child_process.spawn()` allows us to run Python asynchronously without blocking Node.js.
 * - We pass command-line arguments to control signal parameters dynamically.
 * - Standard output (stdout) captures the Python script’s JSON response.
 * 
 * Retrieves oscilloscope measurement data (amplitude, phase).
 * This function calls the Python script to query oscilloscope measurements.
 * 
 * Design Decision:
 * - The oscilloscope communicates via SCPI commands, handled in Python.
 * - Node.js needs to asynchronously retrieve and parse JSON-formatted results.
 * - Using `spawn()` ensures efficient, non-blocking execution.
**/


// import child process
const { spawn } = require('child_process');

exports.sendTestSignal = (req, res) => {
    const { frequency, waveform } = req.body;
    // spawn a child process to execute the Python script
    const pythonProcess = spawn('python3', ['backend/scripts/oscilloscope_control.py', 'test-signal', frequency, waveform]);

    // listen for python output
    pythonProcess.stdout.on('data', (data) => {
        res.json(JSON.parse(data.toString()));
    });

    //handle errors if the python script fails
    pythonProcess.stderr.on('data', (error) => {
        res.status(500).json({ error: error.toString() });
    });
};

exports.getMeasurements = (req, res) => {
    // execute the python script to get oscilloscope measurements
    const pythonProcess = spawn('python3', ['backend/scripts/oscilloscope_control.py', 'get-measurements']);

    // process stdout data from python and return response
    pythonProcess.stdout.on('data', (data) => {
        res.json(JSON.parse(data.toString()));
    });

    // 
    pythonProcess.stderr.on('data', (error) => {
        res.status(500).json({ error: error.toString() });
    });
};
