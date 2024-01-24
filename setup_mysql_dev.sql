-- This script prepares a MySQL server for the project.

-- Check if the hbnb_dev_db database exists; if not, create it.
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

-- Check if the hbnb_dev user exists; if not, create it and set the password.
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';

-- Grant all privileges on the hbnb_dev_db database to the hbnb_dev user.
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';

-- Grant SELECT privilege on the performance_schema database to the hbnb_dev user.
-- This allows hbnb_dev to have SELECT privilege only on performance_schema.
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';

-- Flush privileges to apply the changes immediately.
FLUSH PRIVILEGES;
