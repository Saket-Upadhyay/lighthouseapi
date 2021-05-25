CREATE DATABASE lighthouse;

CREATE TABLE User_Details(
 /*Device_id int primary key auto_increment,*/
 Email_id VARCHAR(20) UNIQUE NOT NULL,
 Pass varchar(10) /*constraint password_check check (pass regexp '^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*]).{8,}$')*/
);

DROP TABLE Captcha;
CREATE TABLE Captcha(
Email_id VARCHAR(20),
Time_generated datetime default current_timestamp,
Capt VARCHAR(4) primary key,
foreign key(Email_id) references User_Details(Email_id) on delete Cascade
);
