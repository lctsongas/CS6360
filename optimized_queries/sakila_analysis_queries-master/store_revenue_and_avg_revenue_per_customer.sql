-- Total revenue and average revenue per customer for each store
WITH store_customer_revenue AS (
  SELECT
    s.store_id,
    c.customer_id,
    SUM(p.amount) AS customer_revenue
  FROM
    payment p
    JOIN rental r ON p.rental_id = r.rental_id
    JOIN customer c ON r.customer_id = c.customer_id
    JOIN inventory i ON r.inventory_id = i.inventory_id
    JOIN store s ON i.store_id = s.store_id
  GROUP BY
    s.store_id,
    c.customer_id
)

SELECT
  store_id,
  COUNT(customer_id) AS total_customers,
  SUM(customer_revenue) AS total_revenue,
  AVG(customer_revenue) AS avg_revenue_per_customer
FROM
  store_customer_revenue
GROUP BY
  store_id;
