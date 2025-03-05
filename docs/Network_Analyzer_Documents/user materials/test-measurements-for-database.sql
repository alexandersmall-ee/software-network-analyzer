-- Database for storing oscilloscope measurement logs
CREATE TABLE measurements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    frequency REAL NOT NULL,
    amplitude REAL NOT NULL,
    phase REAL NOT NULL
);

-- Example query to insert data
INSERT INTO measurements (timestamp, frequency, amplitude, phase) 
VALUES ("2025-03-04T15:00:00Z", 1000, 3.2, 45.5);

-- Example query to retrieve latest measurements
SELECT * FROM measurements ORDER BY timestamp DESC LIMIT 10;
