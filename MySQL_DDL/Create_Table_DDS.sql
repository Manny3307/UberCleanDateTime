USE manny_uber_records_2021;
CREATE TABLE UberDriver(
	DriverID 			INT PRIMARY KEY AUTO_INCREMENT,
    DriverFirstName		VARCHAR(500),
    DriverLastName		VARCHAR(500)
);

CREATE TABLE UberDriverCPVVCertificate(
	DriverCertificateID		INT PRIMARY KEY AUTO_INCREMENT,
    DriverID				INT,
    DriverCertificate		VARCHAR(25),
    FOREIGN KEY(DriverID) REFERENCES UberDriver(DriverID)
);

CREATE TABLE UberDriverContactInfo(
	DriverContactID			INT PRIMARY KEY AUTO_INCREMENT,
    DriverID 				INT,
    DriverContactType		VARCHAR(20),
    DriverContactValue		VARCHAR(500),
    FOREIGN KEY(DriverID) REFERENCES UberDriver(DriverID)
);

CREATE TABLE UberDriverTripRecord(
	DriverID				INT,
	PhoneNumber				INT,
	Email					INT,	
	TripDateTime			DATETIME,
	TripID					VARCHAR(50),	
    TripType				VARCHAR(15),
	TripBaseFare			FLOAT8,
	TripFareCancellation	FLOAT8,
	TripFareMinOrSupplement FLOAT8,
	TripFareSupplement		FLOAT8,
	TripFareWaitTime		FLOAT8,	
	TripServiceFee			FLOAT8,	
	TripTip					FLOAT8,	
	TripTotal       		FLOAT8,
    FOREIGN KEY(DriverID) REFERENCES UberDriver(DriverID),
    FOREIGN KEY(PhoneNumber) REFERENCES UberDriverContactInfo(DriverContactID),
    FOREIGN KEY(Email) REFERENCES UberDriverContactInfo(DriverContactID)
);

CREATE TABLE UberCleaningRecords (
    DriverID 					INT,
    DriverCertificateID			INT,
    DateandTimeofTrip 			VARCHAR(50),
    DateandTimeofClean			VARCHAR(50),
    PassengerSurfacesCleaned 	VARCHAR(5),
    DriverSurfacesCleaned 		VARCHAR(5),
    FOREIGN KEY(DriverID) REFERENCES UberDriver(DriverID),
    FOREIGN KEY(DriverID) REFERENCES UberDriverCPVVCertificate(DriverCertificateID)
);

CREATE TABLE UberRegisteredCar (
	UberCarID					INT PRIMARY KEY AUTO_INCREMENT,
    UberCarRego					VARCHAR(15),
    UberCarVIN					VARCHAR(150),
    UberCarInsuranceProvider	VARCHAR(150),
    UberCarInsuranceType		VARCHAR(50)
);

CREATE TABLE UberDriverCar (
	 DriverID 					INT,
     UberCarID					INT,
     FOREIGN KEY(DriverID) REFERENCES UberDriver(DriverID),
     FOREIGN KEY(UberCarID) REFERENCES UberRegisteredCar(UberCarID)
);