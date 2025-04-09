CREATE DATABASE smart_city;
USE smart_city;

-- Table for regular users
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255)
);

-- Table for admin
CREATE TABLE admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE,
    password VARCHAR(255)
);

-- Table for complaints
CREATE TABLE complaints (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    address TEXT,
    description TEXT,
    image_path VARCHAR(255),
    status VARCHAR(50) DEFAULT 'In Progress',
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

INSERT INTO admins (username, password)
VALUES ('admin@suncity.com', 'admin123');



USE smart_city;

SELECT * FROM users;

SELECT * FROM complaints;
