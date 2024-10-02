# main.py

from db import execute_query

def get_user_city(first_name, last_name):
    query = '''
        SELECT c.first_name, c.last_name, a.address, ci.city
        FROM customer c
        JOIN address a ON c.address_id = a.address_id
        JOIN city ci ON a.city_id = ci.city_id
        WHERE c.first_name = %s AND c.last_name = %s;
    '''
    result = execute_query(query, (first_name, last_name), fetch=True)
    return result[0] if result else None

def insert_user(first_name, last_name, city, address):
    # Додати користувача в таблицю customer
    address_query = '''
        INSERT INTO address (address, city_id) VALUES (%s, (SELECT city_id FROM city WHERE city = %s))
        RETURNING address_id;
    '''
    address_id = execute_query(address_query, (address, city), fetch=True)

    if address_id:
        query = '''
            INSERT INTO customer (first_name, last_name, address_id)
            VALUES (%s, %s, %s);
        '''
        execute_query(query, (first_name, last_name, address_id[0][0]))
    else:
        print(f"Не вдалося додати адресу {address}.")

def create_table():
    create_users_table_query = '''
        CREATE TABLE IF NOT EXISTS customer (
            customer_id SERIAL PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            address_id INT REFERENCES address(address_id)
        );
    '''
    execute_query(create_users_table_query)

def list_users():
    query = "SELECT first_name, last_name FROM customer;"
    users = execute_query(query, fetch=True)
    if users:
        print("Список користувачів у базі даних:")
        for user in users:
            print(f"{user[0]} {user[1]}")
    else:
        print("Користувачів не знайдено.")

def main():
    # Створення таблиці, якщо вона не існує
    create_table()

    # Додати деяких користувачів (можна закоментувати, якщо не потрібно)
    insert_user('Bob', 'Smith', 'Kyiv', 'Main St 1')
    insert_user('Alice', 'Cooper', 'Lviv', 'Main St 2')

    # Відображення всіх користувачів у базі даних
    list_users()

    # Введення імені та прізвища користувача
    first_name = input("Введіть ім'я користувача: ")
    last_name = input("Введіть прізвище користувача: ")

    # Отримання міста та адреси користувача
    user_info = get_user_city(first_name, last_name)

    # Виведення результату
    if user_info:
        address, city = user_info[2], user_info[3]
        print(f"Користувача {first_name} {last_name} знайдено. Адреса: {address}, місто: {city}.")
    else:
        print(f"Користувача з ім'ям {first_name} та прізвищем {last_name} не знайдено.")

if __name__ == "__main__":
    main()
