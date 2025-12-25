-- Active: 1766419035834@@127.0.0.1@3306@project_3
CREATE DATABASE Project_3

use Project_3

create Table Student(
    S_id int primary KEY AUTO_INCREMENT,
    First_Name varchar(10),
    Last_Name VARCHAR(10),
    Email varchar(30) UNIQUE,
    Enrollment_date DATE
    )

create table Course(
    c_id int PRIMARY KEY AUTO_INCREMENT,
    C_name VARCHAR(10),
    credits INT,
    Department VARCHAR(10)
)

CREATE TABLE Enrollments (
    enrollment_id INT PRIMARY KEY AUTO_INCREMENT,
    s_id INT,
    c_id INT,
    grade VARCHAR(5),
    FOREIGN KEY (S_id) REFERENCES Student(S_id),
    FOREIGN KEY (c_id) REFERENCES Course(C_id)
);

Create table Proffessors(
    P_id int PRIMARY KEY,
    p_name varchar(20),
    Department VARCHAR(10)
)
