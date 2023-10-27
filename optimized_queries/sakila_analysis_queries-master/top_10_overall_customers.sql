-- Top 10 overall customers
WITH customer_rental_counts AS (
  SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    COUNT(r.rental_id) AS rental_count
  FROM
    customer c
    JOIN rental r ON c.customer_id = r.customer_id
  GROUP BY
    c.customer_id
),

customer_rental_ranked AS (
  SELECT
    customer_id,
    first_name,
    last_name,
    rental_count,
    RANK() OVER (ORDER BY rental_count DESC) AS overall_rank
  FROM
    customer_rental_counts
)

SELECT
  customer_id,
  first_name,
  last_name,
  rental_count,
  overall_rank
FROM
  customer_rental_ranked
WHERE
  overall_rank <= 10;
