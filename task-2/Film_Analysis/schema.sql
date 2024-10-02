-- Таблиця для зберігання інформації про країни
CREATE TABLE country (
    country_id SERIAL PRIMARY KEY,  -- Унікальний ідентифікатор країни (первинний ключ)
    country VARCHAR(50) NOT NULL UNIQUE,  -- Назва країни (унікальне поле)
    last_update TIMESTAMP NOT NULL DEFAULT NOW()  -- Час останнього оновлення запису (значення за замовчуванням - поточний час)
);

-- Таблиця для зберігання інформації про міста
CREATE TABLE city (
    city_id SERIAL PRIMARY KEY,  -- Унікальний ідентифікатор міста (первинний ключ)
    city VARCHAR(50) NOT NULL,  -- Назва міста
    country_id INT NOT NULL,  -- Ідентифікатор країни, до якої належить місто (зовнішній ключ)
    last_update TIMESTAMP NOT NULL DEFAULT NOW(),  -- Час останнього оновлення запису
    UNIQUE(city, country_id),  -- Унікальність: місто повинно бути унікальним для своєї країни
    FOREIGN KEY (country_id) REFERENCES country(country_id) ON DELETE CASCADE  -- Зовнішній ключ, що посилається на таблицю country
);

-- Таблиця для зберігання інформації про адреси
CREATE TABLE address (
    address_id SERIAL PRIMARY KEY,  -- Унікальний ідентифікатор адреси (первинний ключ)
    address VARCHAR(100) NOT NULL,  -- Текст адреси
    district VARCHAR(50),  -- Район (необов'язкове поле)
    phone VARCHAR(20),  -- Телефонний номер (необов'язкове поле)
    city_id INT NOT NULL,  -- Ідентифікатор міста, до якого належить адреса (зовнішній ключ)
    last_update TIMESTAMP NOT NULL DEFAULT NOW(),  -- Час останнього оновлення запису
    UNIQUE(address, city_id),  -- Унікальність: адреса повинна бути унікальною для свого міста
    FOREIGN KEY (city_id) REFERENCES city(city_id) ON DELETE CASCADE  -- Зовнішній ключ, що посилається на таблицю city
);

-- Таблиця для зберігання інформації про магазини
CREATE TABLE store (
    store_id SERIAL PRIMARY KEY,  -- Унікальний ідентифікатор магазину (первинний ключ)
    manager_staff_id INT,  -- Ідентифікатор менеджера магазину (можливо, посилається на таблицю співробітників)
    address_id INT NOT NULL,  -- Ідентифікатор адреси магазину (зовнішній ключ)
    last_update TIMESTAMP NOT NULL DEFAULT NOW(),  -- Час останнього оновлення запису
    FOREIGN KEY (address_id) REFERENCES address(address_id) ON DELETE CASCADE  -- Зовнішній ключ, що посилається на таблицю address
);

-- Таблиця для зберігання інформації про клієнтів
CREATE TABLE customer (
    customer_id SERIAL PRIMARY KEY,  -- Унікальний ідентифікатор клієнта (первинний ключ)
    store_id INT NOT NULL,  -- Ідентифікатор магазину, в якому зареєстрований клієнт (зовнішній ключ)
    first_name VARCHAR(50) NOT NULL,  -- Ім'я клієнта
    last_name VARCHAR(50) NOT NULL,  -- Прізвище клієнта
    address_id INT NOT NULL,  -- Ідентифікатор адреси клієнта (зовнішній ключ)
    last_update TIMESTAMP NOT NULL DEFAULT NOW(),  -- Час останнього оновлення запису
    FOREIGN KEY (store_id) REFERENCES store(store_id) ON DELETE CASCADE,  -- Зовнішній ключ, що посилається на таблицю store
    FOREIGN KEY (address_id) REFERENCES address(address_id) ON DELETE CASCADE  -- Зовнішній ключ, що посилається на таблицю address
);
