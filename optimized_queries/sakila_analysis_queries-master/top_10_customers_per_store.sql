-- Top 10 customers per store
WITH customer_store_rental_counts AS (
  SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    i.store_id,
    COUNT(r.rental_id) AS rental_count
  FROM
    customer c
    JOIN rental r ON c.customer_id = r.customer_id
    JOIN inventory i ON r.inventory_id = i.inventory_id
  GROUP BY
    c.customer_id,
    i.store_id
),

customer_store_rental_ranked AS (
  SELECT
    customer_id,
    first_name,
    last_name,
    store_id,
    rental_count,
    RANK() OVER (PARTITION BY store_id ORDER BY rental_count DESC) AS store_rank
  FROM
    customer_store_rental_counts
)

SELECT
  customer_id,
  first_name,
  last_name,
  store_id,
  rental_count,
  store_rank
FROM
  customer_store_rental_ranked
WHERE
  store_rank <= 10;
