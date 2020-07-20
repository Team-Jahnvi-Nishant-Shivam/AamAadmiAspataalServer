import psycopg2
import sqlalchemy

from aam_aadmi_aspataal import db


def create(doctor_id: str, patient_id: str, time: str, problem_description: str):
    with db.engine.connect() as connection:
        connection.execute(sqlalchemy.text("""
            INSERT INTO appointment (doctor_id, patient_id, time, problem_description)
                VALUES (:doctor_id, :patient_id, :time, :problem_description)
            """), {
                'doctor_id': doctor_id,
                'patient_id': patient_id,
                'time': time,
                'problem_description': problem_description
            }
        )

def get_latest_appointment_time_for_doctor_or_patient(doctor_id: int, patient_id: int):
    with db.engine.connect() as connection:
        result = connection.execute(sqlalchemy.text("""
            SELECT max(time) AS value
              FROM appointment
             WHERE doctor_id = :doctor_id
              OR patient_id = :patient_id
            """), {
                'doctor_id': doctor_id,
                'patient_id': patient_id
            }
        )
        row = result.fetchone()
        return (row['value'] if row else None)


def get_next_appointment_for_doctor_and_patient(doctor_id: str, patient_id:str, time: str):
    with db.engine.connect() as connection:
        result = connection.execute(sqlalchemy.text("""
            SELECT time AS value
              FROM appointment
             WHERE doctor_id = :doctor_id
              AND patient_id = :patient_id
              AND time > :time
            """), {
                'doctor_id': doctor_id,
                'patient_id': patient_id,
                'time': time
            }
        )
        row = result.fetchone()
        return (row['value'] if row else None)


def get_appointments_for_today_for_doctor(doctor_id: str, start_time: str, end_time: str):
    with db.engine.connect() as connection:
        result = connection.execute(sqlalchemy.text("""
            SELECT a.id, a.time, a.problem_description, p.name, p.firebase_id AS patient_id, p.phone_no
              FROM appointment a
             JOIN patient p
              ON a.patient_id = p.id
             WHERE a.doctor_id = :doctor_id
              AND time >= :start_time
              AND time <= :end_time
             ORDER BY time
              DESC
            """), {
                'doctor_id': doctor_id,
                'start_time': start_time,
                'end_time': end_time
            }
        )
        return [dict(row) for row in result.fetchall()]


def get_appointments_for_today_for_patient(patient_id: str, start_time: str, end_time: str):
    with db.engine.connect() as connection:
        result = connection.execute(sqlalchemy.text("""
            SELECT a.id, a.time, a.problem_description, d.name, d.firebase_id AS doctor_id, d.email_id
              FROM appointment a
             JOIN doctor d
              ON a.doctor_id = d.id
             WHERE a.patient_id = :patient_id
              AND time >= :start_time
              AND time <= :end_time
             ORDER BY time
              DESC
            """), {
                'patient_id': patient_id,
                'start_time': start_time,
                'end_time': end_time
            }
        )
        return [dict(row) for row in result.fetchall()]


def get_past_appointments_for_doctor(doctor_id: str, end_time: str):
    with db.engine.connect() as connection:
        result = connection.execute(sqlalchemy.text("""
            SELECT a.id, a.time, a.problem_description, p.name, p.firebase_id AS patient_id, p.phone_no, pr.prescription_details
              FROM appointment a
             JOIN patient p
              ON a.patient_id = p.id
            LEFT JOIN prescription pr
              ON a.id = pr.appointment_id
             WHERE a.doctor_id = :doctor_id
              AND time <= :end_time
             ORDER BY time
              DESC
            """), {
                'doctor_id': doctor_id,
                'end_time': end_time
            }
        )
        return [dict(row) for row in result.fetchall()]


def get_past_appointments_for_patient(patient_id: str, end_time: str):
    with db.engine.connect() as connection:
        result = connection.execute(sqlalchemy.text("""
            SELECT a.id, a.time, a.problem_description, d.name, d.firebase_id AS doctor_id, d.email_id, pr.prescription_details
              FROM appointment a
             JOIN doctor d
              ON a.doctor_id = d.id
            LEFT JOIN prescription pr
              ON a.id = pr.appointment_id
             WHERE a.patient_id = :patient_id
              AND time <= :end_time
             ORDER BY time
              DESC
            """), {
                'patient_id': patient_id,
                'end_time': end_time
            }
        )
        return [dict(row) for row in result.fetchall()]


def get_all_appointments_for_doctor(doctor_id: str):
    with db.engine.connect() as connection:
        result = connection.execute(sqlalchemy.text("""
            SELECT a.id, a.time, a.problem_description, p.name, p.firebase_id AS patient_id, p.phone_no, pr.prescription_details
              FROM appointment a
             JOIN patient p
              ON a.patient_id = p.id
            LEFT JOIN prescription pr
              ON a.id = pr.appointment_id
             WHERE a.doctor_id = :doctor_id
             ORDER BY time
              DESC
            """), {
                'doctor_id': doctor_id
            }
        )
        return [dict(row) for row in result.fetchall()]


def get_all_appointments_for_patient(patient_id: str):
    with db.engine.connect() as connection:
        result = connection.execute(sqlalchemy.text("""
            SELECT a.id, a.time, a.problem_description, d.name, d.firebase_id AS doctor_id, d.email_id, pr.prescription_details
              FROM appointment a
             JOIN doctor d
              ON a.doctor_id = d.id
            LEFT JOIN prescription pr
              ON a.id = pr.appointment_id
             WHERE a.patient_id = :patient_id
             ORDER BY time
              DESC
            """), {
                'patient_id': patient_id
            }
        )
        return [dict(row) for row in result.fetchall()]


def get_appointment_by_id(appointment_id: int):
    with db.engine.connect() as connection:
        result = connection.execute(sqlalchemy.text("""
            SELECT a.id, a.time, a.problem_description, pr.prescription_details
              FROM appointment a
            LEFT JOIN prescription pr
              ON a.id = pr.appointment_id
             WHERE a.id = :appointment_id
            """), {
                'appointment_id': appointment_id
            }
        )
        row = result.fetchone()
        return (dict(row) if row else None)
