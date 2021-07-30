DROP PROCEDURE IF EXISTS InsertJSONCleaningRecord;
CREATE DEFINER=`admin`@`%` PROCEDURE `InsertJSONCleaningRecord`(OUT ProcCode TEXT)
BEGIN
	
    sp: BEGIN
        DECLARE ProcDriverID INT DEFAULT 0;
        DECLARE ProcDriverCertificateID INT DEFAULT 0;
        DECLARE ProcDriverName VARCHAR(200);
        
        DECLARE tempCounter INT DEFAULT 0;
        DECLARE whileCounter INT DEFAULT 0;
        
        DECLARE code CHAR(5) DEFAULT '00000';
		DECLARE msg TEXT;
		DECLARE nrows INT;
		DECLARE result TEXT;
        
        DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
		BEGIN
		  GET DIAGNOSTICS CONDITION 1
			code = RETURNED_SQLSTATE, msg = MESSAGE_TEXT;
		END;
        
        SAVEPOINT spoint;
        
        START TRANSACTION;
        
				SET whileCounter = 1;
				
				CREATE TEMPORARY TABLE tblHoldDriverID
				(
					ID						INT PRIMARY KEY AUTO_INCREMENT,
					DriverID				INT,
					DriverCertificateID		INT,
					DriverName				VARCHAR(200)
				);
				
				INSERT INTO tblHoldDriverID(DriverID, DriverCertificateID, DriverName)
				SELECT DISTINCT 
					ud.DriverID,
					udcpv.DriverCertificateID,
					ut.Driver_name
				FROM
					UberTempCleaningRecords ut
					INNER JOIN UberDriver ud ON ut.Driver_name = ud.DriverFirstName
					INNER JOIN UberDriverCPVVCertificate udcpv ON udcpv.DriverID = ud.DriverID;
				
				SET tempCounter = (SELECT COUNT(*) FROM tblHoldDriverID);
				
				IF code = '00000' THEN
					GET DIAGNOSTICS nrows = ROW_COUNT;
					SET result = CONCAT('Insert succeeded to tblHoldDriverID, row count = ', nrows);
				ELSE
					SET result = CONCAT('Insert failed to tblHoldDriverID, error = ',code,', message = ', msg);
					SET ProcCode = result;
					ROLLBACK TO spoint;
					LEAVE sp;
				END IF;
				
				WHILE whileCounter <= tempCounter DO
					
					SET ProcDriverID = (SELECT DriverID FROM tblHoldDriverID tblHoldDriverID WHERE ID = whileCounter);
					SET ProcDriverCertificateID = (SELECT DriverCertificateID FROM tblHoldDriverID tblHoldDriverID WHERE ID = whileCounter);
					SET ProcDriverName = (SELECT DriverName FROM tblHoldDriverID tblHoldDriverID WHERE ID = whileCounter);
					
					INSERT INTO UberCleaningRecords(
								DriverID, 
								DriverCertificateID, 
								DateandTimeofTrip, 
								DateandTimeofClean, 
								PassengerSurfacesCleaned, 
								DriverSurfacesCleaned)
					SELECT 
						ProcDriverID,
						ProcDriverCertificateID,
						Date_and_time_of_trip,
						Date_and_Time_of_clean,  
						Passenger_hightouch_surfaces_cleaned, 
						Driver_hightouch_surfaces_cleaned
					FROM
						UberTempCleaningRecords
					WHERE
						Driver_name = ProcDriverName;
					
					SET whileCounter = whileCounter + 1;
				END WHILE;
			
				IF code = '00000' THEN
					GET DIAGNOSTICS nrows = ROW_COUNT;
					SET result = CONCAT('Insert succeeded to UberCleaningRecords, row count = ', nrows);
				ELSE
					SET result = CONCAT('Insert failed to UberCleaningRecords, error = ',code,', message = ', msg);
					ROLLBACK TO spoint;
					LEAVE sp;
				END IF;
				
				SET ProcCode = result;
		COMMIT;
	
    TRUNCATE TABLE UberTempCleaningRecords;
    DROP TEMPORARY TABLE tblHoldDriverID;
    
    END;
    
END