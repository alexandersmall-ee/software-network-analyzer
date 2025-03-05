/**
 * signalController - Handles API communication with the oscilloscope
 * uses python backend via `child_process.spawn()`
 *     - `spawn()` is used instead of `exec()` to handle large data streams efficiently
 *     - JSON parsing ensures frontend receives structured responses
 *     - errors are captured at multiple levels (invalid input, Python execution, response formatting)
 **/

const { spawn } = require('child_process');

/**
 * sends test signal to the oscilloscope
 * 
 * route: POST /api/test-signal
 * request: { "frequency": 1000, "waveform": "SIN" }
 */
exports.sendTestSignal = (req, res) => {
    const { frequency, waveform } = req.body;

    // validate request body parameters
    if (!frequency || !waveform) {
        return res.status(400).json({
            error: "Missing required parameters",
            details: "Both 'frequency' and 'waveform' are required."
        });
    }

    // execute python script with arguments
    const pythonProcess = spawn('python3', ['backend/scripts/oscilloscope_control.py', 'test-signal', frequency, waveform]);

    // stdout data
    pythonProcess.stdout.on('data', (data) => {
        try {
            const parsedData = JSON.parse(data.toString().trim());
            res.json(parsedData);
        } catch (error) {
            res.status(500).json({
                error: "Invalid JSON response from Python",
                details: error.message
            });
        }
    });

    // stderr output (errors)
    pythonProcess.stderr.on('data', (error) => {
        res.status(500).json({
            error: "Python execution error",
            details: error.toString()
        });
    });

    // process exit errors
    pythonProcess.on('exit', (code) => {
        if (code !== 0) {
            res.status(500).json({
                error: "Python script exited with error",
                exitCode: code
            });
        }
    });
};

/**
 * retrieves oscilloscope measurement data (amplitude, phase)
 *
 * route: GET /api/measurements
 * response: { "timestamp": "...", "amplitude": 3.2, "phase": 45.5 }
 */
exports.getMeasurements = (req, res) => {
    const pythonProcess = spawn('python3', ['backend/scripts/oscilloscope_control.py', 'get-measurements']);

    // stdout data from Python
    pythonProcess.stdout.on('data', (data) => {
        try {
            const parsedData = JSON.parse(data.toString().trim());
            res.json(parsedData);
        } catch (error) {
            res.status(500).json({
                error: "Invalid JSON response from Python",
                details: error.message
            });
        }
    });

    //  stderr output (errors)
    pythonProcess.stderr.on('data', (error) => {
        res.status(500).json({
            error: "Python execution error",
            details: error.toString()
        });
    });

    // process exit errors
    pythonProcess.on('exit', (code) => {
        if (code !== 0) {
            res.status(500).json({
                error: "Python script exited with error",
                exitCode: code
            });
        }
    });
};
