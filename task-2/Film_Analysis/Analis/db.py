# db.py

import psycopg2
from psycopg2 import OperationalError, IntegrityError

def connect_db():
    try:
        conn = psycopg2.connect(
            dbname='pagila',
            user='postgres',
            password='129056',
            host='localhost',
            port='5432'
        )
        return conn
    except OperationalError as e:
        print(f"Не вдалося підключитися до бази даних: {e}")
        return None

def execute_query(query, params=None, fetch=False):
    conn = connect_db()
    if conn is None:
        return None

    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute(query, params if params else ())

        if fetch:
            result = cursor.fetchall()
            conn.commit()  # Фіксуємо транзакцію після вибірки (для INSERT з RETURNING)
            return result

        conn.commit()  # Фіксуємо транзакцію для запитів, які не потребують вибірки
    except IntegrityError as ie:
        print(f"IntegrityError: {ie}")
        conn.rollback()
    except Exception as e:
        print(f"Помилка виконання запиту: {e}")
        conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()