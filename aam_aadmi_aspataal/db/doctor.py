import psycopg2
import sqlalchemy

from aam_aadmi_aspataal import db


def create(firebase_id: str):
    with db.engine.connect() as connection:
        connection.execute(sqlalchemy.text("""
            INSERT INTO doctor (firebase_id)
                VALUES (:firebase_id)
            """), {
                'firebase_id': firebase_id
            }
        )

def get_by_token(firebase_id: str):
    with db.engine.connect() as connection:
        result = connection.execute(sqlalchemy.text("""
            SELECT *
              FROM DOCTOR
             WHERE firebase_id = :firebase_id
            """), {
                'firebase_id': firebase_id
            }
        )
        row = result.fetchone()
        return dict(row) if row else None

def update_record(id: int, name: str, email_id: str, specialisation: str, registration_no: str):
    with db.engine.connect() as connection:
        result = connection.execute(sqlalchemy.text("""
            UPDATE doctor
              SET name = :name,
                  email_id = :email_id,
                  specialisation = :specialisation,
                  registration_no = :registration_no
             WHERE id = :id
            """), {
                'id': id,
                'name': name,
                'email_id': email_id,
                'specialisation': specialisation,
                'registration_no': registration_no
            }
        )