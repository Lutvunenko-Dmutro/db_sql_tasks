SELECT 
    film.title AS "Назва фільму", 
    COUNT(rental.rental_id) AS "Кількість оренд"
FROM 
    film
JOIN 
    inventory ON film.film_id = inventory.film_id
JOIN 
    rental ON inventory.inventory_id = rental.inventory_id
GROUP BY 
    film.title
ORDER BY 
    COUNT(rental.rental_id) DESC
LIMIT 5;
