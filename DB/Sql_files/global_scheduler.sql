SET GLOBAL event_scheduler = ON;
Drop event captcha_update;
CREATE EVENT captcha_update
ON SCHEDULE EVERY 30 second
starts current_timestamp
DO
  delete from Captcha
  WHERE Time_generated<=current_timestamp()-180;