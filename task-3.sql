-- 1. Загальна кількість фільмів у кожній категорії
SELECT c.name AS category_name, COUNT(f.film_id) AS total_films
FROM category c
JOIN film_category fc ON c.category_id = fc.category_id
JOIN film f ON fc.film_id = f.film_id
GROUP BY c.name;

-- 2. Середня тривалість фільмів у кожній категорії
SELECT c.name AS category_name, AVG(f.length) AS average_duration
FROM category c
JOIN film_category fc ON c.category_id = fc.category_id
JOIN film f ON fc.film_id = f.film_id
GROUP BY c.name;

-- 3. Мінімальна та максимальна тривалість фільмів
SELECT MIN(length) AS min_duration, MAX(length) AS max_duration
FROM film;

-- 4. Загальна кількість клієнтів
SELECT COUNT(*) AS total_customers
FROM customer;

-- 5. Сума платежів по кожному клієнту
SELECT CONCAT(c.first_name, ' ', c.last_name) AS customer_name, SUM(p.amount) AS total_payments
FROM customer c
JOIN payment p ON c.customer_id = p.customer_id
GROUP BY c.customer_id;

-- 6. П'ять клієнтів з найбільшою сумою платежів
SELECT CONCAT(c.first_name, ' ', c.last_name) AS customer_name, SUM(p.amount) AS total_payments
FROM customer c
JOIN payment p ON c.customer_id = p.customer_id
GROUP BY c.customer_id
ORDER BY total_payments DESC
LIMIT 5;

-- 7. Загальна кількість орендованих фільмів кожним клієнтом
SELECT CONCAT(c.first_name, ' ', c.last_name) AS customer_name, COUNT(r.rental_id) AS total_rentals
FROM customer c
JOIN rental r ON c.customer_id = r.customer_id
GROUP BY c.customer_id;

-- 8. Середній вік фільмів у базі даних (для Postgre)
SELECT AVG(EXTRACT(YEAR FROM CURRENT_DATE) - f.release_year) AS average_age
FROM film f;

-- 9. Кількість фільмів, орендованих за певний період
SELECT COUNT(*) AS total_rentals
FROM rental
WHERE rental_date BETWEEN '2024-01-01' AND '2024-12-31';  -- Змініть дати на ваші

-- 10. Сума платежів по кожному місяцю
SELECT TO_CHAR(payment_date, 'YYYY-MM') AS month, SUM(amount) AS total_payments
FROM payment
GROUP BY month
ORDER BY month;

-- 11. Максимальна сума платежу, здійснена клієнтом
SELECT customer_id, MAX(amount) AS max_payment
FROM payment
GROUP BY customer_id;

-- 12. Середня сума платежів для кожного клієнта
SELECT CONCAT(c.first_name, ' ', c.last_name) AS customer_name, AVG(p.amount) AS average_payment
FROM customer c
JOIN payment p ON c.customer_id = p.customer_id
GROUP BY c.customer_id;

-- 13. Кількість фільмів у кожному рейтингу (rating)
SELECT rating, COUNT(*) AS total_films
FROM film
GROUP BY rating;

-- 14. Середня сума платежів по кожному магазину (store)
SELECT s.store_id, AVG(p.amount) AS average_payment
FROM store s
JOIN inventory i ON s.store_id = i.store_id
JOIN rental r ON i.inventory_id = r.inventory_id
JOIN payment p ON r.rental_id = p.rental_id
GROUP BY s.store_id;
