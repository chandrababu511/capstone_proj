# load_database.py

import pandas as pd
import sqlite3

df = pd.read_csv(
    "cleaned_books.csv"
)

conn = sqlite3.connect(
    "books.db"
)

cursor = conn.cursor()

# categories table

cursor.execute("""
CREATE TABLE IF NOT EXISTS categories(
category_id INTEGER PRIMARY KEY,
category_name TEXT UNIQUE
)
""")

# books table

cursor.execute("""
CREATE TABLE IF NOT EXISTS books(
book_id INTEGER PRIMARY KEY,
title TEXT,
price_gbp REAL,
price_inr REAL,
rating INTEGER,
in_stock INTEGER,
category_id INTEGER,
FOREIGN KEY(category_id)
REFERENCES categories(category_id)
)
""")

# insert category

categories = df["category"].unique()

for cat in categories:

    cursor.execute(
        """
        INSERT OR IGNORE INTO categories
        (category_name)
        VALUES(?)
        """,
        (cat,)
    )

conn.commit()

cat_df = pd.read_sql(
    "SELECT * FROM categories",
    conn
)

mapping = dict(
    zip(
        cat_df["category_name"],
        cat_df["category_id"]
    )
)

df["category_id"] = df["category"].map(
    mapping
)

books_df = df[
    [
        "title",
        "price_gbp",
        "price_inr",
        "rating",
        "in_stock",
        "category_id"
    ]
]

books_df.to_sql(
    "books",
    conn,
    if_exists="append",
    index=False
)

conn.close()

print("books.db created")