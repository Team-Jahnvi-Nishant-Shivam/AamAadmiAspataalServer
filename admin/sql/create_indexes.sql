BEGIN;

CREATE INDEX doctor_id_patient_id_index_appointment ON appointment (doctor_id, patient_id);
CREATE INDEX appointment_id_index_prescription ON prescription (appointment_id);
CREATE INDEX patient_id_index_report ON report (patient_id);

COMMIT;
