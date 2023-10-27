-- Top 5 most popular film categories for each store
WITH store_category_rentals AS (
  SELECT
    s.store_id,
    c.name AS category_name,
    COUNT(r.rental_id) AS rental_count
  FROM
    rental r
    JOIN inventory i ON r.inventory_id = i.inventory_id
    JOIN store s ON i.store_id = s.store_id
    JOIN film f ON i.film_id = f.film_id
    JOIN film_category fc ON f.film_id = fc.film_id
    JOIN category c ON fc.category_id = c.category_id
  GROUP BY
    s.store_id,
    c.name
)

, store_category_rentals_ranked AS (
  SELECT
    store_id,
    category_name,
    rental_count,
    RANK() OVER (PARTITION BY store_id ORDER BY rental_count DESC) AS rental_rank
  FROM
    store_category_rentals
)

SELECT
  *
FROM
  store_category_rentals_ranked
WHERE
  rental_rank <= 5;
