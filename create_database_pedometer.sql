DROP DATABASE IF EXISTS pedometer;
CREATE DATABASE pedometer;
USE pedometer;
CREATE TABLE WalkingSession(
    ID INT NOT NULL AUTO_INCREMENT,
    Type CHAR(1) NOT NULL,
    Mean DOUBLE NOT NULL,
    StartTime DATETIME NOT NULL,
    StopTime DATETIME NOT NULL,
    Duration DOUBLE NOT NULL,
    CountOfSteps INT NOT NULL,
    MET FLOAT NOT NULL,
    Weight INT NOT NULL,
    Calories DOUBLE NOT NULL,
    
    PRIMARY KEY (ID)
	   
);
