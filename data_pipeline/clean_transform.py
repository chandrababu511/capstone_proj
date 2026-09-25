# clean_transform.py

import pandas as pd

GBP_TO_INR = 105.50

df = pd.read_csv("raw_books.csv")

# price
df["price_gbp"] = (
    df["price"]
    .str.replace("£", "", regex=False)
)

df["price_gbp"] = pd.to_numeric(
    df["price_gbp"],
    errors="coerce"
)

# median imputation
median_price = df["price_gbp"].median()

df["price_gbp"].fillna(
    median_price,
    inplace=True
)

# ratings
rating_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

df["rating"] = df["star_rating"].map(
    rating_map
)

median_rating = df["rating"].median()

df["rating"].fillna(
    median_rating,
    inplace=True
)

# stock
df["in_stock"] = df["availability"].str.contains(
    "In stock",
    case=False
)

# INR conversion
df["price_inr"] = (
    df["price_gbp"]
    * GBP_TO_INR
)

df.to_csv(
    "cleaned_books.csv",
    index=False
)

print("cleaned_books.csv created")