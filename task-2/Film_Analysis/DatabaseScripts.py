import psycopg2
import os
from prettytable import PrettyTable

# Параметри підключення
connection_params = {
    'dbname': 'pagila',       # Назва вашої бази даних
    'user': 'postgres',       # Ваше ім'я користувача
    'password': '129056',     # Ваш пароль
    'host': 'localhost',      # Хост
    'port': '5432',           # Порт
}

# Функція для виконання SQL-запиту
def execute_query(query):
    try:
        # Підключення до бази даних
        with psycopg2.connect(**connection_params) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                # Якщо запит виконує SELECT, повертаємо результати
                if query.strip().upper().startswith("SELECT"):
                    results = cursor.fetchall()
                    return results, cursor.description  # Повертаємо також опис стовпців
                else:
                    return "Query executed successfully.", None
    except Exception as e:
        return f"An error occurred: {e}", None

# Функція для виконання SQL-запиту з файлу
def execute_query_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            query = file.read()
            return execute_query(query)
    except Exception as e:
        return f"An error occurred while reading the file: {e}", None

# Функція для виводу результатів у таблиці
def print_results_in_table(results, description):
    if description is None:
        print("No results to display.")
        return
    
    table = PrettyTable()
    table.field_names = [desc[0] for desc in description]  # Додаємо назви стовпців
    for row in results:
        table.add_row(row)  # Додаємо рядки
    print(table)

# Встановлення відносного шляху до директорії з SQL-файлами
scripts_directory = 'Film_Analysis'  # Відносний шлях до директорії

# Виконання SQL-запитів
queries = {
    "films_with_categories": "SELECT f.title AS \"Назва фільму\", c.name AS \"Категорія\" "
                             "FROM film f "
                             "JOIN film_category fc ON f.film_id = fc.film_id "
                             "JOIN category c ON fc.category_id = c.category_id;", # У Мене токо тиким образом робить 
    # "films_with_categories": os.path.join(scripts_directory, 'films_with_categories.sql'), # Цей код не робить хотя довжен
    "films_rented_by_john": os.path.join(scripts_directory, 'films_rented_by_john_farnsworth.sql'),
    "top_5_popular_films": os.path.join(scripts_directory, 'top_5_popular_films.sql'),
}

# Виконання запитів та виведення результатів
for query_name, query in queries.items():
    print(f"\n{query_name.replace('_', ' ').title()}:")
    if query.startswith("SELECT"):  # Якщо запит SQL
        results, description = execute_query(query)
    else:  # Якщо шлях до файлу
        results, description = execute_query_from_file(query)
    
    if results:
        print_results_in_table(results, description)
    else:
        print("No results found.")
