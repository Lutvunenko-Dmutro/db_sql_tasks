SELECT 
    film.title AS "Назва фільму", 
    rental.last_update AS "Дата оренди"
FROM 
    customer
JOIN 
    rental ON customer.customer_id = rental.customer_id
JOIN 
    inventory ON rental.inventory_id = inventory.inventory_id
JOIN 
    film ON inventory.film_id = film.film_id
WHERE 
    customer.first_name = 'JOHN' 
    AND customer.last_name = 'FARNSWORTH';
