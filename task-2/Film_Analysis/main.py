# main.py

from models import add_customer, delete_customer, update_customer_address, list_countries

def main_menu():
    while True:
        print("\nОберіть дію:")
        print("1. Додати клієнта")
        print("2. Видалити клієнта")
        print("3. Оновити адресу клієнта")
        print("4. Показати країни")
        print("5. Вихід")

        action = input("Ваш вибір (введіть цифру): ").strip()

        if action == '1':
            first_name = input("Введіть ім'я клієнта: ").strip()
            last_name = input("Введіть прізвище клієнта: ").strip()
            address = input("Введіть адресу клієнта: ").strip()
            city = input("Введіть місто клієнта: ").strip()
            store_id = input("Введіть ID магазину: ").strip()
            add_customer(first_name, last_name, address, city, store_id)

        elif action == '2':
            first_name = input("Введіть ім'я клієнта для видалення: ").strip()
            last_name = input("Введіть прізвище клієнта для видалення: ").strip()
            delete_customer(first_name, last_name)

        elif action == '3':
            first_name = input("Введіть ім'я клієнта для оновлення адреси: ").strip()
            last_name = input("Введіть прізвище клієнта для оновлення адреси: ").strip()
            new_address = input("Введіть нову адресу: ").strip()
            update_customer_address(first_name, last_name, new_address)

        elif action == '4':
            list_countries()

        elif action == '5':
            print("Вихід...")
            break

        else:
            print("Невірний вибір, спробуйте ще раз.")

if __name__ == "__main__":
    main_menu()
