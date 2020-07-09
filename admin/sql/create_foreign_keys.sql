BEGIN;

ALTER TABLE appointment
    ADD CONSTRAINT appointment_doctor_id_foreign_key
    FOREIGN KEY (doctor_id)
    REFERENCES doctor (id)
    ON DELETE CASCADE;

ALTER TABLE appointment
    ADD CONSTRAINT appointment_patient_id_foreign_key
    FOREIGN KEY (patient_id)
    REFERENCES patient (id)
    ON DELETE CASCADE;

ALTER TABLE prescription
    ADD CONSTRAINT prescription_appointment_id_foreign_key
    FOREIGN KEY (appointment_id)
    REFERENCES appointment (id)
    ON DELETE CASCADE;

ALTER TABLE report
    ADD CONSTRAINT report_patient_id_foreign_key
    FOREIGN KEY (patient_id)
    REFERENCES patient (id)
    ON DELETE CASCADE;

COMMIT;
