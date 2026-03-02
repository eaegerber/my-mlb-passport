CREATE DATABASE IF NOT EXISTS mlb_passport;
USE mlb_passport;

CREATE TABLE IF NOT EXISTS ping_test (
  id INT AUTO_INCREMENT PRIMARY KEY,
  message VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO ping_test (message) VALUES ('hello from init.sql');