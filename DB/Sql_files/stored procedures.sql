/*EDIT 1*/
/*extract_details to extract info*/
/*AuthenticateUser2 to authenticate user*/
/*Inscpt to insert captcha for registered user*/

/*Retriving User Details*/
DELIMITER $$
USE health_management_system $$
CREATE PROCEDURE extract_details( 
  IN id varchar(20) ,
  OUT hash_val varchar(20),
  OUT cptt varchar(4))
BEGIN IF ( 
  select exists (select 1 from Captcha where id=Email_id) 
) THEN set hash_val := (select Pass from User_Details where id=Email_id);
set cptt := (select Capt from Captcha where id=Email_id );
ELSE 
  set hash_val:='1';
  set cptt:='1';
END IF;
END$$
DELIMITER ;

/*Auth2 */
DELIMITER $$
USE health_management_system $$
CREATE PROCEDURE AuthenticateUser2 (
  IN email VARCHAR(20),
  IN passkey varchar(30),
  OUT msg int)
BEGIN IF ( 
  select exists (select 1 from User_Details where Email_id = email and Pass=passkey ) 
) THEN set msg := 0;
ELSE set msg:= 1;
END IF;
END$$
DELIMITER ;




/* CREATE USER */
DELIMITER $$
USE lighthouse $$
CREATE PROCEDURE Create_User( 
  IN Email varchar(20), 
  IN Passkey varchar(10),
  OUT msg int)
BEGIN 
DECLARE EXIT HANDLER FOR 3819 set msg := 1;
IF ( 
  select exists (select 1 from User_Details where Email_id = Email) 
) THEN SET msg :=1;
ELSE 
  insert into User_Details (Email_id,Pass) values (Email,Passkey);
  set msg :=0;
END IF;
END$$
DELIMITER ;

/* AUTHENTICATE USER */
DELIMITER $$
USE lighthouse $$
CREATE PROCEDURE AuthenticateUser (
  IN email VARCHAR(20),
  OUT id int)
BEGIN IF ( 
  select exists (select Device_id from User_Details where Email_id = email  ) 
) THEN set id := (select Device_id from User_Details where Email_id = email);
ELSE set id := 0;
END IF;
END$$
DELIMITER ;

/* Generating new captcha for registered user */
DELIMITER $$
USE lighthouse $$
CREATE PROCEDURE Generate_Captcha(
  IN id int,
  INOUT cpt varchar(4))
BEGIN
DECLARE EXIT HANDLER FOR 1062 set cpt:= '----';
set cpt :=upper(RIGHT(MD5(CURRENT_TIMESTAMP),4));
insert into captcha (Device_id,Capt) values (id,cpt);
END$$
DELIMITER ;

/* Time Limit Check */

DELIMITER $$
USE lighthouse $$
CREATE PROCEDURE CptCheck( 
  IN id int ,
  IN received_capt varchar(4),
  OUT msg int)
BEGIN IF ( 
  select exists (select 1 from Captcha where id=Device_id and Capt=received_capt) 
) THEN set msg :=0;
ELSE 
  set msg:=1;
END IF;
END$$
DELIMITER ;

