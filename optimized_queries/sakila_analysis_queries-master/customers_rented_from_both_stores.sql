-- Customers who have rented films from both stores
SELECT
  c.customer_id,
  c.first_name,
  c.last_name
FROM
  customer c
WHERE
  EXISTS (
    SELECT
      1
    FROM
      rental r
      JOIN inventory i ON r.inventory_id = i.inventory_id
      JOIN store s ON i.store_id = s.store_id
    WHERE
      r.customer_id = c.customer_id
      AND s.store_id = 1
  )
  AND EXISTS (
    SELECT
      1
    FROM
      rental r
      JOIN inventory i ON r.inventory_id = i.inventory_id
      JOIN store s ON i.store_id = s.store_id
    WHERE
      r.customer_id = c.customer_id
      AND s.store_id = 2
  );
