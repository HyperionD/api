create database if not exists note;

use note;

CREATE TABLE IF NOT EXISTS note (
	id INT PRIMARY KEY AUTO_INCREMENT,
	title VARCHAR(255),
	content LONGTEXT, 
	datetime VARCHAR(255)
);


CREATE TABLE IF NOT EXISTS label (
	id INT PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(255)
);


CREATE TABLE IF NOT EXISTS notelabel (
	id INT PRIMARY KEY AUTO_INCREMENT,
	note_id INT,
	label_id INT
);
