--
-- File generated with SQLiteStudio v3.3.3 on Sun Apr 2 21:13:50 2023
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: dashboard
CREATE TABLE dashboard (
    user_id                    INTEGER      PRIMARY KEY,
    name                       VARCHAR (75),
    temperature_threshhold     INT,
    humidity_threshhold        INT,
    light_intensity_threshhold INT
);


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
