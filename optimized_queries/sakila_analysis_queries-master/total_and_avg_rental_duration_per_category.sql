-- Total and average rental duration per film category
SELECT
  c.name AS category_name,
  SUM(f.rental_duration) AS total_rental_duration,
  AVG(f.rental_duration) AS avg_rental_duration
FROM
  film f
  JOIN film_category fc ON f.film_id = fc.film_id
  JOIN category c ON fc.category_id = c.category_id
GROUP BY
  c.name;
