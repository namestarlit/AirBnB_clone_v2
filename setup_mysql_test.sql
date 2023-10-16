-- MySQL setup test
-- creates database hbnb_test_db
CREATE DATABASE IF NOT EXISTS hbnb_test_db;
-- create user hbnb_test with pass hbnb_test_pwd
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';
-- grant all privileges to hbnb_test_db database
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';
-- grant select privileges to performance_schema database
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';
