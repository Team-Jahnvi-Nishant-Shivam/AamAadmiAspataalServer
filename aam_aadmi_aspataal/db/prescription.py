import psycopg2
import sqlalchemy

from aam_aadmi_aspataal import db

def create(appointment_id: str, prescription_details: str):
    with db.engine.connect() as connection:
        connection.execute(sqlalchemy.text("""
            INSERT INTO prescription (appointment_id, prescription_details)
                VALUES (:appointment_id, :prescription_details)
            """), {
                'appointment_id': appointment_id,
                'prescription_details': prescription_details
            }
        )
