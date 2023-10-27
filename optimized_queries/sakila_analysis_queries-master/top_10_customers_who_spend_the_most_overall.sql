-- Top 10 customers who spend the most overall
WITH customer_total_spent AS (
  SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    SUM(p.amount) AS total_spent
  FROM
    customer c
    JOIN payment p ON c.customer_id = p.customer_id
  GROUP BY
    c.customer_id,
    c.first_name,
    c.last_name
)

SELECT
  customer_id,
  first_name,
  last_name,
  total_spent
FROM
  customer_total_spent
ORDER BY
  total_spent DESC
LIMIT 10;
