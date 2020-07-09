BEGIN;

ALTER TABLE doctor ADD CONSTRAINT doctor_primary_key PRIMARY KEY (id);
ALTER TABLE patient ADD CONSTRAINT patient_primary_key PRIMARY KEY (id);
ALTER TABLE appointment ADD CONSTRAINT appointment_primary_key PRIMARY KEY (id);
ALTER TABLE prescription ADD CONSTRAINT prescription_primary_key PRIMARY KEY (id);
ALTER TABLE report ADD CONSTRAINT report_primary_key PRIMARY KEY (id);

COMMIT;
