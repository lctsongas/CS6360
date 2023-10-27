-- Top 10 most rented films
WITH film_rental_counts AS (
  SELECT
    f.film_id,
    f.title,
    COUNT(r.rental_id) AS rental_count
  FROM
    rental r
    JOIN inventory i ON r.inventory_id = i.inventory_id
    JOIN film f ON i.film_id = f.film_id
  GROUP BY
    f.film_id,
    f.title
)

SELECT
  *
FROM
  film_rental_counts
ORDER BY
  rental_count DESC
LIMIT 10;
