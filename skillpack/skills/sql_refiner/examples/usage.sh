# Example: Convert question to SQL
skillpack sql-refiner --question "How many active users signed up in the last 30 days" --dialect postgres

# Example: BigQuery dialect
skillpack sql-refiner --question "Get top 10 orders by amount" --dialect bigquery

# Example: Snowflake dialect
skillpack sql-refiner --question "Calculate average order value per customer" --dialect snowflake
