BEGIN;

CREATE TABLE doctor (
  id                    SERIAL, --PK
  firebase_id           VARCHAR NOT NULL,
  name                  VARCHAR,
  email_id              VARCHAR,
  specialisation        VARCHAR,
  registration_no       VARCHAR
);
ALTER TABLE doctor ADD CONSTRAINT doctor_firebase_id_key UNIQUE (firebase_id);
ALTER TABLE doctor ADD CONSTRAINT doctor_registration_no_key UNIQUE (registration_no);

CREATE TABLE patient (
  id                    SERIAL, --PK
  firebase_id           VARCHAR NOT NULL,
  name                  VARCHAR,
  phone_no              VARCHAR
);
ALTER TABLE patient ADD CONSTRAINT patient_firebase_id_key UNIQUE (firebase_id);

CREATE TABLE appointment ( 
  id                    SERIAL, -- PK
  doctor_id             INTEGER NOT NULL, -- FK to doctor.id
  patient_id            INTEGER NOT NULL, -- FK to patient.id
  time                  TIMESTAMP,
  problem_description   VARCHAR
);

CREATE TABLE prescription ( 
  id                    SERIAL, -- PK
  appointment_id        INTEGER NOT NULL, -- FK to appointment.id
  prescription_details  VARCHAR
);

CREATE TABLE report ( 
  id                    SERIAL, -- PK
  patient_id            INTEGER NOT NULL, -- FK to patient.id
  image_url             VARCHAR NOT NULL,
  report_details        VARCHAR
);
ALTER TABLE report ADD CONSTRAINT report_image_url_key UNIQUE (image_url);

COMMIT;
