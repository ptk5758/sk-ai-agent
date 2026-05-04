import psycopg
from uuid import UUID
def get_ingredients():
    with psycopg.connect("dbname=sk_ax user=dev password=dev1234 host=localhost") as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                        SELECT
                            id,
                            name,
                            quantity,
                            unit,
                            created_at,
                            updated_at
                        FROM ingredients
                        """)
            rows = cursor.fetchall()
    return rows

def create_ingredient(name: str, quantity: float, unit: str) -> UUID :
    with psycopg.connect("dbname=sk_ax user=dev password=dev1234 host=localhost") as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                           INSERT INTO ingredients
                           (
                           "name",
                           quantity,
                           unit
                           )
                           VALUES
                           (
                           %s,
                           %s,
                           %s
                           )
                           RETURNING id
                           """,
                           (name, quantity, unit))
            return cursor.fetchone()
    