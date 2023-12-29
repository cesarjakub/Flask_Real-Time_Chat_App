CREATE TABLE users(
id int PRIMARY KEY AUTO_INCREMENT,
name VARCHAR(20) not null,
email VARCHAR(50) not null,
password VARCHAR(255) not null
);

CREATE TABLE message(
id int PRIMARY KEY AUTO_INCREMENT,
SenderID INT not null,
MessageText VARCHAR(255) not null,
RoomID int not null,
Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (SenderID) REFERENCES users(id),
);