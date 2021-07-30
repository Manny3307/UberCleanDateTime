INSERT INTO UberDriver (DriverFirstName, DriverLastName) VALUES ('Manmeet', 'Arora');

INSERT INTO UberDriverCPVVCertificate (DriverID, DriverCertificate) VALUES(1, 'DC631236');

INSERT INTO UberDriverContactInfo (DriverID, DriverContactType, DriverContactValue) VALUES(1, 'Mobile', '0416438047');
INSERT INTO UberDriverContactInfo (DriverID, DriverContactType, DriverContactValue) VALUES(1, 'Home', '0352092600');
INSERT INTO UberDriverContactInfo (DriverID, DriverContactType, DriverContactValue) VALUES(1, 'Email', 'manmeetarora@yahoo.com');
INSERT INTO UberDriverContactInfo (DriverID, DriverContactType, DriverContactValue) VALUES(1, 'Address', '5 Simpson Circuit, Armstrong Creek, VIC 3217');
INSERT INTO UberDriverContactInfo (DriverID, DriverContactType, DriverContactValue) VALUES(1, 'License', '008696539');

INSERT INTO UberRegisteredCar (UberCarRego, UberCarVIN, UberCarInsuranceProvider, UberCarInsuranceType) 
            VALUES('1JU-5NC', 'MR053REH205284934', 'Real Insurance', 'Comprehensive');

INSERT INTO UberDriverCar (DriverID, UberCarID) VALUES(1, 1);
