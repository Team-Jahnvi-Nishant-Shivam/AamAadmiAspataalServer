import psycopg2
import sqlalchemy

from aam_aadmi_aspataal import db

def create(patient_id: str, image_url: str, report_details: str):
    with db.engine.connect() as connection:
        connection.execute(sqlalchemy.text("""
            INSERT INTO report (patient_id, image_url, report_details)
                VALUES (:patient_id, :image_url, :report_details)
            """), {
                'patient_id': patient_id,
                'image_url': image_url,
                'report_details': report_details
            }
        )


def get_by_patient_id(patient_id: str):
    with db.engine.connect() as connection:
        result = connection.execute(sqlalchemy.text("""
            SELECT image_url, report_details
              FROM report
             WHERE patient_id = :patient_id
            """), {
                'patient_id': patient_id
            }
        )
        return [dict(row) for row in result.fetchall()]
