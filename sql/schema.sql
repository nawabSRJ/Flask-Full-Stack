-- USERS

CREATE TABLE users(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(250) NOT NULL,
    phone VARCHAR(10) UNIQUE NOT NULL,
    age INT NOT NULL,
    gender VARCHAR(20) NOT NULL,
    course VARCHAR(50) NOT NULL,
    photo VARCHAR(255) DEFAULT NULL,   
    is_verified TINYINT(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
)

-- ADMIN

CREATE TABLE admin (
    id       INT AUTO_INCREMENT PRIMARY KEY,
    email    VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(250) NOT NULL               -- hashed
);

-- CREATING ADMIN RECORD
INSERT INTO admin (email, password) 
VALUES ('admin@flaskapp.com', 'scrypt:32768:8:1$qQtwnhYgi9BdtoYb$063deb32f72f68358d3fcb47be7da722b855b2fa75b7d621ac737f06741e7ee7e88e441e12cd89d5d100dbe897be7abc89d4c00e254d5d4c14f1c6a4e98fdaba');