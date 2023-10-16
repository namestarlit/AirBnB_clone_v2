-- MySQL setup development
-- creates database hbnb_dev_db
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
-- create user hbnb_dev with pass hbnb_dev_pwd
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';
-- grant all privileges to hbnb_dev_db database
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';
-- grant select privileges to performance_schema database
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';
