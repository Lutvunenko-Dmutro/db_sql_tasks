-- SQL-запит для отримання списку фільмів з їх категоріями та тривалістю
SELECT 
    film.title AS "Назва фільму", 
    film.length AS "Тривалість", 
    category.name AS "Категорія"
FROM 
    film
JOIN 
    film_category ON film.film_id = film_category.film_id
JOIN 
    category ON film_category.category_id = category.category_id;
