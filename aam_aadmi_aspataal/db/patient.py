import psycopg2
import sqlalchemy

from aam_aadmi_aspataal import db


def create(firebase_id: str):
    with db.engine.connect() as connection:
        connection.execute(sqlalchemy.text("""
            INSERT INTO patient (firebase_id)
                VALUES (:firebase_id)
            """), {
                'firebase_id': firebase_id
            }
        )

def get_by_token(firebase_id: str):
    with db.engine.connect() as connection:
        result = connection.execute(sqlalchemy.text("""
            SELECT *
              FROM patient
             WHERE firebase_id = :firebase_id
            """), {
                'firebase_id': firebase_id
            }
        )
        row = result.fetchone()
        return dict(row) if row else None

def update_record(id: int, name: str, phone_no: str):
    with db.engine.connect() as connection:
        result = connection.execute(sqlalchemy.text("""
            UPDATE patient
              SET name = :name,
                  phone_no = :phone_no
             WHERE id = :id
            """), {
                'id': id,
                'name': name,
                'phone_no': phone_no
            }
        )