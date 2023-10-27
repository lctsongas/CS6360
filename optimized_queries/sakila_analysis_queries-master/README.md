# Sakila Sample Database Analysis

This repository contains a collection of SQL queries used to analyze the Sakila Sample Database. The queries are designed to be efficient and optimized for execution time, resource utilization, query plan, index usage, join strategies, subquery and CTE usage, data retrieval, aggregation, and grouping.

* [Table of Contents](#table-of-contents)
  * [Queries](#queries)
    + [1.1 Top Rankings](#11-top-rankings)
      - [1.1.1 Top 10 Most Rented Films](#111-top-10-most-rented-films)
      - [1.1.2 Top 5 Popular Categories per Store](#112-top-5-popular-categories-per-store)
      - [1.1.3 Top 10 Overall Customers](#113-top-10-overall-customers)
      - [1.1.4 Top 10 Customers per Store](#114-top-10-customers-per-store)
    + [1.2 Revenue and Rentals](#12-revenue-and-rentals)
      - [1.2.1 Total Revenue per Store](#121-total-revenue-per-store)
      - [1.2.2 Store Revenue and Average Revenue per Customer](#122-store-revenue-and-average-revenue-per-customer)
      - [1.2.3 Store Total Rentals and Average Rentals per Customer](#123-store-total-rentals-and-average-rentals-per-customer)
    + [1.3 Customers](#13-customers)
      - [1.3.1 Customers Rented from Both Stores](#131-customers-rented-from-both-stores)
      - [1.3.2 Top 10 Customers Who Spend the Most per Store](#132-top-10-customers-who-spend-the-most-per-store)
      - [1.3.3 Top 10 Customers Who Spend the Most Overall](#133-top-10-customers-who-spend-the-most-overall)
    + [1.4 Films and Actors](#14-films-and-actors)
      - [1.4.1 Total and Average Rental Duration per Category](#141-total-and-average-rental-duration-per-category)
      - [1.4.2 Actors in More Than 10 Films](#142-actors-in-more-than-10-films)
  * [Authorship](#Authorship)
  * [References](#References)

## Queries 

### 1.1 Top Rankings 

#### 1.1.1 Top 10 Most Rented Films 

- [Query file](./top_10_most_rented_films.sql)
- **Technical explanation**: Calculates the top 10 most rented films by rental count. This query joins the `rental`, `inventory`, and `film` tables, groups the results by film ID, title, and description, and uses the `COUNT` function to aggregate the rental count.
- **Why is this the best approach?**: The query directly calculates the rental count for each film using a simple join and aggregation strategy. This results in optimized execution time and resource utilization.
- **Business case**: Identifying the top 10 most rented films can be used to understand customer preferences and trends, allowing for better inventory management and targeted marketing efforts.

[Back to Top](#sakila-sample-database-analysis)

#### 1.1.2 Top 5 Popular Categories per Store

- [Query file](./top_5_popular_categories_per_store.sql)
- **Technical explanation**: Finds the top 5 most popular film categories for each store based on rental count. The query joins the `rental`, `inventory`, `film`, `film_category`, `category`, and `store` tables, groups the results by store ID, category name, and store location, and uses the `COUNT` function to aggregate the rental count for each category.
- **Why is this the best approach?**: The query directly calculates the rental count for each category in each store, using a simple join and aggregation strategy. This results in optimized execution time and resource utilization.
- **Business case**: Understanding the top 5 popular categories per store can help management make informed decisions about inventory allocation and marketing efforts specific to each store location.

[Back to Top](#sakila-sample-database-analysis)

#### 1.1.3 Top 10 Overall Customers 

- [Query file](./top_10_overall_customers.sql)
- **Technical explanation**: Calculates the top 10 overall customers by rental count. The query joins the `rental`, `inventory`, `customer`, and `store` tables, groups the results by customer ID, first name, last name, and store location, and uses the `COUNT` function to aggregate the rental count for each customer.
- **Why is this the best approach?**: This query directly calculates the rental count for each customer using a simple join and aggregation strategy. This results in optimized execution time and resource utilization.
- **Business case**: Identifying the top 10 overall customers can help the business understand and reward their most loyal customers, encouraging customer retention and fostering positive relationships.

[Back to Top](#sakila-sample-database-analysis)

#### 1.1.4 Top 10 Customers per Store 

- [Query file](./top_10_customers_per_store.sql)
- **Technical explanation**: Calculates the top 10 customers for each store by rental count. The query joins the `rental`, `inventory`, `customer`, and `store` tables, groups the results by store ID, customer ID, first name, last name, and store location, and uses the `COUNT` function to aggregate the rental count for each customer.
- **Why is this the best approach?**: This query directly calculates the rental count for each customer in each store using a simple join and aggregation strategy. This results in optimized execution time and resource utilization.
- **Business case**: Identifying the top 10 customers per store can help store managers understand and reward their most loyal customers, encouraging customer retention and fostering positive relationships.

[Back to Top](#sakila-sample-database-analysis)

### 1.2 Revenue and Rentals

#### 1.2.1 Total Revenue per Store

- [Query file](./total_revenue_per_store.sql)
- **Technical explanation**: Calculates the total revenue per store. The query joins the `payment`, `rental`, `inventory`, and `store` tables, groups the results by store ID and location, and uses the `SUM` function to aggregate the total revenue for each store.
- **Why is this the best approach?**: This query directly calculates the total revenue for each store using a simple join and aggregation strategy. This results in optimized execution time and resource utilization.
- **Business case**: Understanding the total revenue per store can help management make informed decisions about store performance, budget allocation, and resource management.

[Back to Top](#sakila-sample-database-analysis)

#### 1.2.2 Store Revenue and Average Revenue per Customer 

- [Query file](./store_revenue_and_avg_revenue_per_customer.sql)
- **Technical explanation**: Calculates the total revenue and average revenue per customer for each store. The query joins the `payment`, `rental`, `inventory`, `customer`, and `store` tables, groups the results by store ID and location, and uses the `SUM` and `AVG` functions to aggregate the total revenue and average revenue per customer for each store.
- **Why is this the best approach?**: This query directly calculates the total revenue and average revenue per customer for each store using a simple join and aggregation strategy. This results in optimized execution time and resource utilization.
- **Business case**: Understanding the total revenue and average revenue per customer for each store can help management assess the effectiveness of marketing strategies, customer retention efforts, and revenue generation tactics.

[Back to Top](#sakila-sample-database-analysis)

#### 1.2.3 Store Total Rentals and Average Rentals per Customer 

- [Query file](./store_total_rentals_and_avg_rentals_per_customer.sql)
- **Technical explanation**: Calculates the total rentals and average rentals per customer for each store. The query joins the `rental`, `inventory`, `customer`, and `store` tables, groups the results by store ID and location, and uses the `COUNT` and `AVG` functions to aggregate the total rentals and average rentals per customer for each store.
- **Why is this the best approach?**: This query directly calculates the total rentals and average rentals per customer for each store using a simple join and aggregation strategy. This results in optimized execution time and resource utilization.
- **Business case**: Understanding the total rentals and average rentals per customer for each store can help management evaluate customer engagement and rental trends, allowing for better inventory management and targeted marketing efforts.

[Back to Top](#sakila-sample-database-analysis)

### 1.3 Customers

#### 1.3.1 Customers Rented from Both Stores 

- [Query file](./customers_rented_from_both_stores.sql)
- **Technical explanation**: Identifies customers who have rented from both stores. The query joins the `rental`, `inventory`, `customer`, and `store` tables, groups the results by customer ID, first name, last name, and store ID, and uses the `HAVING` clause to filter customers who rented from both stores.
- **Why is this the best approach?**: This query directly identifies customers who rented from both stores using a simple join and filtering strategy. This results in optimized execution time and resource utilization.
- **Business case**: Identifying customers who rented from both stores can help management understand customer behavior patterns, allowing for better customer segmentation and targeted marketing efforts.

[Back to Top](#sakila-sample-database-analysis)

#### 1.3.2 Top 10 Customers Who Spend the Most per Store 

- [Query file](./top_10_customers_most_spent_per_store.sql)
- **Technical explanation**: Calculates the top 10 customers who spend the most in each store. The query joins the `payment`, `rental`, `inventory`, `customer`, and `store` tables, groups the results by store ID, customer ID, first name, last name, and store location, and uses the `SUM` function to aggregate the total spending for each customer.
- **Why is this the best approach?**: This query directly calculates the total spending for each customer in each store using a simple join and aggregation strategy. This results in optimized execution time and resource utilization.
- **Business case**: Identifying the top 10 customers who spend the most per store can help store managers understand and reward their high-value customers, encouraging customer retention and fostering positive relationships.

[Back to Top](#sakila-sample-database-analysis)

#### 1.3.3 Top 10 Customers Who Spend the Most Overall 

- [Query file](./top_10_customers_who_spend_the_most_overall.sql)
- **Technical explanation**: Calculates the top 10 customers who spend the most overall across all stores. The query joins the `payment`, `rental`, `inventory`, `customer`, and `store` tables, groups the results by customer ID, first name, last name, and store location, and uses the `SUM` function to aggregate the total spending for each customer.
- **Why is this the best approach?**: This query directly calculates the total spending for each customer across all stores using a simple join and aggregation strategy. This results in optimized execution time and resource utilization.
- **Business case**: Identifying the top 10 customers who spend the most overall can help the business understand and reward their high-value customers, encouraging customer retention and fostering positive relationships.

[Back to Top](#sakila-sample-database-analysis)

### 1.4 Films and Actors

#### 1.4.1 Total and Average Rental Duration per Category 

- [Query file](./total_and_avg_rental_duration_per_category.sql)
- **Technical explanation**: Calculates the total and average rental duration for each film category. The query joins the `rental`, `inventory`, `film`, `film_category`, and `category` tables, groups the results by category name, and uses the `SUM` and `AVG` functions to aggregate the total and average rental duration for each category.
- **Why is this the best approach?**: This query directly calculates the total and average rental duration for each category using a simple join and aggregation strategy. This results in optimized execution time and resource utilization.
- **Business case**: Understanding the total and average rental duration per category can help management assess customer preferences and rental trends, allowing for better inventory management and targeted marketing efforts.

[Back to Top](#sakila-sample-database-analysis)

#### 1.4.2 Actors in More Than 10 Films 

- [Query file](./actors_in_more_than_10_films.sql)
- **Technical explanation**: Identifies actors who have appeared in more than 10 films. The query joins the `actor`, `film_actor`, and `film` tables, groups the results by actor ID, first name, and last name, and uses the `COUNT` function to aggregate the film count for each actor. The `HAVING` clause filters actors with more than 10 films.
- **Why is this the best approach?**: This query directly identifies actors who have appeared in more than 10 films using a simple join and filtering strategy. This results in optimized execution time and resource utilization.
- **Business case**: Identifying actors who have appeared in more than 10 films can help the business understand which actors are popular among customers, allowing for better film selection and marketing efforts.

[Back to Top](#sakila-sample-database-analysis)

## Authorship

This analysis and the accompanying files were created by Alberto F. Hernandez. If you have any questions, suggestions, or issues, please feel free to contact me at ah8664383@gmail.com.

[Back to Top](#sakila-sample-database-analysis)

## References

Hunter, J. (2007). Matplotlib: A 2D graphics environment. IEEE COMPUTER SOC.

Kanz, A. (2020). Klib.

Kluyver, T., Ragan-Kelley, B., Perez, F., Granger, B., Bussonnier, M., & Frederic, J. et al. (2016). Jupyter Notebooks - a publishing format for reproducible computational workflows. In Positioning and Power in Academic Publishing: Players, Agents and Agendas (pp. 87-90). Netherlands; IOS Press. Retrieved 19 May 2022, from https://eprints.soton.ac.uk/403913/.

Oracle Corporation. (2019). Sakila sample database. Oracle Corporation.

The pandas development team. (2020). pandas-dev/pandas: Pandas. Zenodo.

van Rossum, G. (1991). Python. Python Software Foundation.

[Back to Top](#sakila-sample-database-analysis)

