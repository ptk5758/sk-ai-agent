import psycopg

def get_ingredients():
    with psycopg.connect("dbname=sk_ax user=dev password=dev1234 host=localhost") as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                        SELECT
                            id,
                            name,
                            quantity,
                            unit,
                            category,
                            location,
                            expiration_date,
                            created_at,
                            updated_at
                        FROM ingredients
                        """)
            rows = cursor.fetchall()
    return rows

def create_ingredient(name: str, quantity: float, unit: str):
    with psycopg.connect("dbname=sk_ax user=dev password=dev1234 host=localhost") as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                           INSERT INTO ingredients
                           (
                           "name",
                           quantity,
                           unit,
                           expiration_date
                           )
                           VALUES
                           (
                           %s,
                           %s,
                           %s,
                           NULL
                           )
                           RETURNING id
                           """,
                           (name, quantity, unit))
            return cursor.fetchone()
    