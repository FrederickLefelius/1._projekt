CREATE DATABASE IF NOT EXISTS heste_data;
USE heste_data;

CREATE TABLE IF NOT EXISTS sensor_readings (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    timestamp        DATETIME DEFAULT CURRENT_TIMESTAMP,
    humidity         FLOAT,
    temperature      FLOAT,
    fan_on           BOOLEAN,
    window_open      BOOLEAN,
    smoke_detected   BOOLEAN,
    horse_down_count INT
);
