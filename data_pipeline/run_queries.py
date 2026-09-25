# run_queries.py

import sqlite3
import pandas as pd

conn = sqlite3.connect(
    "books.db"
)

queries = {

"query1": """
SELECT *
FROM books
WHERE rating = 5
""",

"query2": """
SELECT title, price_gbp
FROM books
ORDER BY price_gbp DESC
""",

"query3": """
SELECT *
FROM books
LIMIT 10
""",

"query4": """
SELECT DISTINCT rating
FROM books
""",

"query5": """
SELECT *
FROM books
WHERE price_gbp
BETWEEN 20 AND 40
""",

"join_query": """
SELECT
b.title,
c.category_name,
b.rating
FROM books b
JOIN categories c
ON b.category_id =
c.category_id
ORDER BY rating DESC
LIMIT 10
"""
}

for name, query in queries.items():

    df = pd.read_sql(
        query,
        conn
    )

    print("\n")
    print("="*40)
    print(name)
    print("="*40)

    print(df.head())

    df.to_csv(
        f"{name}.csv",
        index=False
    )

# pd.read_sql example

df_sql1 = pd.read_sql(
"""
SELECT *
FROM books
WHERE rating=5
""",
conn
)

df_sql2 = pd.read_sql(
"""
SELECT *
FROM books
LIMIT 10
""",
conn
)

# pd.merge example

books = pd.read_sql(
    "SELECT * FROM books",
    conn
)

categories = pd.read_sql(
    "SELECT * FROM categories",
    conn
)

merged = pd.merge(
    books,
    categories,
    on="category_id"
)

print("\nMERGED DATAFRAME")

print(
    merged[
    [
        "title",
        "category_name",
        "rating"
    ]
    ].head()
)

conn.close()
