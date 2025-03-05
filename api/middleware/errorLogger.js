const fs = require('fs');
const path = require('path');

const logFile = path.join(__dirname, '../logs/api-errors.log');

const errorLogger = (err, req, res, next) => {
    const logEntry = `[${new Date().toISOString()}] ${req.method} ${req.originalUrl} - ${err.message}\n`;

    // Write to log file asynchronously
    fs.appendFile(logFile, logEntry, (error) => {
        if (error) console.error("Failed to write to log file:", error);
    });

    // Standardized error response
    res.status(500).json({
        error: "Internal Server Error",
        details: err.message
    });
};

module.exports = errorLogger;
