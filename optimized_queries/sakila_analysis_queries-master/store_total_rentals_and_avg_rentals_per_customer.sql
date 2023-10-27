-- Total number of rentals and average rentals per customer for each store
WITH store_customer_rentals AS (
  SELECT
    s.store_id,
    r.customer_id,
    COUNT(r.rental_id) AS rental_count
  FROM
    rental r
    JOIN inventory i ON r.inventory_id = i.inventory_id
    JOIN store s ON i.store_id = s.store_id
  GROUP BY
    s.store_id,
    r.customer_id
)

SELECT
  store_id,
  COUNT(customer_id) AS total_customers,
  SUM(rental_count) AS total_rentals,
  AVG(rental_count) AS avg_rentals_per_customer
FROM
  store_customer_rentals
GROUP BY
  store_id;
