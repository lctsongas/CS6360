-- Top 10 customers who spend the most per store
WITH customer_store_total_spent AS (
  SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    i.store_id,
    SUM(p.amount) AS total_spent
  FROM
    customer c
    JOIN payment p ON c.customer_id = p.customer_id
    JOIN rental r ON p.rental_id = r.rental_id
    JOIN inventory i ON r.inventory_id = i.inventory_id
  GROUP BY
    c.customer_id,
    c.first_name,
    c.last_name,
    i.store_id
),

customer_store_spent_ranked AS (
  SELECT
    customer_id,
    first_name,
    last_name,
    store_id,
    total_spent,
    RANK() OVER (PARTITION BY store_id ORDER BY total_spent DESC) AS store_rank
  FROM
    customer_store_total_spent
)

SELECT
  customer_id,
  first_name,
  last_name,
  store_id,
  total_spent,
  store_rank
FROM
  customer_store_spent_ranked
WHERE
  store_rank <= 10;
