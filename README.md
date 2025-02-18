# Film Analysis Database

## Опис
Цей проект є базою даних для аналізу фільмів, яка зберігає інформацію про фільми, категорії, клієнтів та магазини. Проект дозволяє користувачам ефективно управляти фільмами, а також отримувати дані про оренду та популярність фільмів.

## Структура проекту

Проект містить такі файли:

- **main.py**: Основний скрипт для взаємодії з базою даних. Використовується для додавання та пошуку клієнтів.
- **DatabaseScripts.py**: Скрипт для виконання SQL-запитів до бази даних, включаючи запити на отримання фільмів, категорій та інших даних. Результати відображаються у зручному форматі таблиці.
- **client_database.py**: Скрипт для роботи з клієнтами в базі даних. **`main.py` і `client_database.py` є однаковими.**
- **Analis.py**: Скрипт, що дозволяє користувачеві вводити ім'я та прізвище, щоб знайти адресу, пов'язану з цим клієнтом.

## Налаштування

1. **Встановлення PostgreSQL**:
   - Якщо у вас ще немає PostgreSQL, завантажте та встановіть [PostgreSQL](https://www.postgresql.org/download/).
   - Переконайтеся, що у вас є база даних під назвою `pagila`. Якщо її немає, створіть базу даних, використовуючи команду:
     ```sql
     CREATE DATABASE pagila;
     ```

2. **Налаштування підключення до бази даних**:
   - Відкрийте файл `DatabaseScripts.py` і `db.py` та переконайтеся, що параметри підключення (`dbname`, `user`, `password`) відповідають вашій базі даних.
   - Переконайтеся, що ці параметри вказують на вашу базу даних, як показано в наступному прикладі:
     ```python
     conn = psycopg2.connect(
         dbname='pagila',
         user='your_username',
         password='your_password',
         host='localhost',
         port='5432'
     )
     ```
## Використання

1. **Додавання клієнтів**:
   - Запустіть `main.py` або `client_database.py` для додавання клієнтів у базу даних.
   - Введіть ім'я, прізвище, адресу та місто клієнта.

2. **Пошук клієнтів**:
   - Запустіть `Analis.py` і введіть ім'я та прізвище, щоб знайти адресу клієнта.

3. **Виконання SQL-запитів**:
   - Запустіть `DatabaseScripts.py` для виконання запитів до бази даних. Доступні запити включають:
     - Список фільмів з категоріями.
     - Фільми, які були орендовані певним клієнтом.
     - Топ-5 популярних фільмів.

## Вимоги
- Python 3.x
- psycopg2 для роботи з PostgreSQL:
  ```bash
  pip install psycopg2
