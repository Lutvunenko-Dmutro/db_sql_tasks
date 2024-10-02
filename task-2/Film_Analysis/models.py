# models.py

from db import execute_query

def get_country_id(country_name):
    country_query = "SELECT country_id FROM country WHERE country = %s;"
    country_result = execute_query(country_query, (country_name,), fetch=True)

    if country_result:
        return country_result[0][0]
    else:
        print(f"Країна '{country_name}' не знайдена.")
        return None

def check_address_exists(address_id):
    query = "SELECT COUNT(*) FROM address WHERE address_id = %s;"
    result = execute_query(query, (address_id,), fetch=True)
    return result[0][0] > 0 if result else False

def get_or_add_address(address, city, country_name="Країна не призначена"):
    country_id = get_country_id(country_name)

    if country_id is None:
        insert_country_query = "INSERT INTO country (country, last_update) VALUES (%s, now()) RETURNING country_id;"
        try:
            country_result = execute_query(insert_country_query, (country_name,), fetch=True)
            if country_result:
                country_id = country_result[0][0]
                print(f"Країну '{country_name}' успішно додано з country_id {country_id}.")
            else:
                print(f"Не вдалося додати країну '{country_name}'.")
                return None
        except Exception as e:
            print(f"Помилка при додаванні країни: {e}")
            return None

    # Перевірити, чи місто вже існує
    city_query = "SELECT city_id FROM city WHERE city = %s;"
    city_result = execute_query(city_query, (city,), fetch=True)

    if not city_result:
        # Якщо місто не існує, додати його
        insert_city_query = "INSERT INTO city (city, country_id, last_update) VALUES (%s, %s, now()) RETURNING city_id;"
        try:
            city_insert_result = execute_query(insert_city_query, (city, country_id), fetch=True)
            if city_insert_result:
                city_id = city_insert_result[0][0]
                print(f"Місто '{city}' успішно додано з city_id {city_id}.")
            else:
                print(f"Не вдалося додати місто '{city}'.")
                return None
        except Exception as e:
            print(f"Помилка при додаванні міста: {e}")
            return None
    else:
        city_id = city_result[0][0]
        print(f"Місто '{city}' вже існує з city_id {city_id}.")

    # Перевірити, чи адреса вже існує
    check_existing_address_query = "SELECT address_id FROM address WHERE address = %s AND city_id = %s;"
    existing_address = execute_query(check_existing_address_query, (address, city_id), fetch=True)

    if existing_address:
        address_id = existing_address[0][0]
        print(f"Адреса '{address}' вже існує з address_id {address_id}.")
        return address_id
    else:
        # Додати адресу з використанням ON CONFLICT для уникнення порушення унікальності
        address_query = """
            INSERT INTO address (address, district, phone, city_id, last_update) 
            VALUES (%s, %s, %s, %s, now()) 
            ON CONFLICT (address, city_id) DO NOTHING 
            RETURNING address_id;
        """
        try:
            address_insert_result = execute_query(address_query, (address, '', 'unknown', city_id), fetch=True)
            if address_insert_result:
                address_id = address_insert_result[0][0]
                print(f"Адресу '{address}' успішно додано з address_id {address_id}.")
                return address_id
            else:
                # Якщо адреса вже існує, отримати її address_id
                existing_address = execute_query(check_existing_address_query, (address, city_id), fetch=True)
                if existing_address:
                    address_id = existing_address[0][0]
                    print(f"Адреса '{address}' вже існує з address_id {address_id}.")
                    return address_id
                else:
                    print(f"Не вдалося додати адресу '{address}'.")
                    return None
        except IntegrityError as ie:
            print(f"IntegrityError під час додавання адреси: {ie}")
            # Спробувати отримати address_id знову
            existing_address = execute_query(check_existing_address_query, (address, city_id), fetch=True)
            if existing_address:
                address_id = existing_address[0][0]
                print(f"Адреса '{address}' вже існує з address_id {address_id}.")
                return address_id
            else:
                return None
        except Exception as e:
            print(f"Помилка під час додавання адреси: {e}")
            return None

def add_customer(first_name, last_name, address, city, store_id):
    # Переконайтеся, що store_id є числом
    try:
        store_id = int(store_id)
    except ValueError:
        print("ID магазину повинен бути числом.")
        return

    address_id = get_or_add_address(address, city)

    if address_id is None:
        print("Не вдалося отримати або додати адресу. Клієнта не буде додано.")
        return

    # Перевірка наявності address_id в таблиці address
    if not check_address_exists(address_id):
        print(f"Адреса з address_id {address_id} не існує в таблиці address. Клієнта не буде додано.")
        return

    insert_customer_query = """
        INSERT INTO customer (store_id, first_name, last_name, address_id, last_update) 
        VALUES (%s, %s, %s, %s, now()) 
        RETURNING customer_id;
    """
    try:
        customer_result = execute_query(insert_customer_query, (store_id, first_name, last_name, address_id), fetch=True)
        if customer_result:
            customer_id = customer_result[0][0]
            print(f"Клієнта {first_name} {last_name} успішно додано з customer_id {customer_id} та ID магазину {store_id}!")
        else:
            print("Помилка при додаванні клієнта.")
    except Exception as e:
        print(f"Помилка виконання запиту на додавання клієнта: {e}")

def delete_customer(first_name, last_name):
    delete_query = "DELETE FROM customer WHERE first_name = %s AND last_name = %s RETURNING customer_id;"
    try:
        delete_result = execute_query(delete_query, (first_name, last_name), fetch=True)
        if delete_result:
            customer_id = delete_result[0][0]
            print(f"Клієнта {first_name} {last_name} успішно видалено з customer_id {customer_id}!")
        else:
            print(f"Клієнта {first_name} {last_name} не знайдено.")
    except Exception as e:
        print(f"Помилка виконання запиту на видалення клієнта: {e}")

def update_customer_address(first_name, last_name, new_address):
    customer_query = "SELECT customer_id, address_id FROM customer WHERE first_name = %s AND last_name = %s;"
    customer_result = execute_query(customer_query, (first_name, last_name), fetch=True)

    if not customer_result:
        print(f"Клієнт {first_name} {last_name} не знайдений.")
        return

    customer_id, current_address_id = customer_result[0]

    # Отримати city_id для поточної адреси
    city_query = "SELECT city_id FROM address WHERE address_id = %s;"
    city_result = execute_query(city_query, (current_address_id,), fetch=True)

    if not city_result:
        print(f"Місто для address_id {current_address_id} не знайдено.")
        return

    city_id = city_result[0][0]

    # Отримати назву міста з city_id
    get_city_name_query = "SELECT city FROM city WHERE city_id = %s;"
    city_name_result = execute_query(get_city_name_query, (city_id,), fetch=True)

    if not city_name_result:
        print(f"Місто з city_id {city_id} не знайдено.")
        return

    city_name = city_name_result[0][0]

    # Перевірити, чи нова адреса вже існує
    check_existing_address_query = "SELECT address_id FROM address WHERE address = %s AND city_id = %s;"
    existing_address = execute_query(check_existing_address_query, (new_address, city_id), fetch=True)

    if existing_address:
        new_address_id = existing_address[0][0]
        print(f"Адреса '{new_address}' вже існує з address_id {new_address_id}. Оновимо адресу клієнта на існуючу адресу.")
    else:
        # Додати нову адресу
        new_address_id = get_or_add_address(new_address, city_name)
        if new_address_id:
            print(f"Нову адресу '{new_address}' успішно додано з address_id {new_address_id}.")
        else:
            print("Не вдалося додати нову адресу. Адресу клієнта не буде оновлено.")
            return

    # Оновити адресу клієнта
    update_address_query = "UPDATE customer SET address_id = %s, last_update = now() WHERE customer_id = %s;"
    try:
        execute_query(update_address_query, (new_address_id, customer_id))
        print(f"Адресу клієнта {first_name} {last_name} успішно оновлено!")
    except Exception as e:
        print(f"Помилка виконання запиту на оновлення адреси: {e}")

def list_countries():
    country_query = "SELECT country_id, country FROM country;"
    countries = execute_query(country_query, fetch=True)

    if countries:
        print("Доступні країни:")
        for country_id, country in countries:
            print(f"{country_id}: {country}")
    else:
        print("Не вдалося отримати список країн.")
