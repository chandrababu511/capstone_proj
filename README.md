#---------------------------------------------------------------------------------
# Data Pipeline Module
#---------------------------------------------------------------------------------
## Project Overview
#---------------------------------------------------------------------------------
This module implements a complete data engineering pipeline using the **Books to Scrape** website. The project demonstrates web scraping, data cleaning, feature engineering, relational database design, SQL querying, and integration between SQLite and Pandas.

The pipeline performs the following tasks:

1. Scrapes book data using Requests and BeautifulSoup.
2. Cleans and transforms raw data.
3. Converts book prices from GBP to INR using a fixed project-defined exchange rate.
4. Stores the cleaned data in a normalized SQLite database.
5. Executes SQL queries demonstrating database operations.
6. Reads query results back into Pandas.
7. Reproduces SQL joins using Pandas `merge()`.

---

# Project Structure

```text
data_pipeline/
│
├── scrape_books.py
├── clean_transform.py
├── load_database.py
├── run_queries.py
├── raw_books.csv
├── cleaned_books.csv
├── books.db
├── query1.csv
├── query2.csv
├── query3.csv
├── query4.csv
├── query5.csv
├── join_query.csv
└── README.md
```

---

# Technologies Used

- Python
- Requests
- BeautifulSoup4
- Pandas
- SQLite3

---

# Installation

Install the required packages:

```bash
pip install requests beautifulsoup4 pandas
```

---

# Running the Pipeline

Execute the scripts in the following order:

### Step 1: Scrape Data

```bash
python scrape_books.py
```

Output:

```text
raw_books.csv
```

---

### Step 2: Clean and Transform Data

```bash
python clean_transform.py
```

Output:

```text
cleaned_books.csv
```

---

### Step 3: Load Data into SQLite Database

```bash
python load_database.py
```

Output:

```text
books.db
```

---

### Step 4: Run SQL Queries

```bash
python run_queries.py
```

Output:

```text
query1.csv
query2.csv
query3.csv
query4.csv
query5.csv
join_query.csv
```

---

# Data Source

Dataset scraped from:

```text
https://books.toscrape.com/
```

The first five pages of the catalog were scraped using Requests and BeautifulSoup.

---

# Data Collected

Each book record contains:

| Column | Description |
|----------|----------|
| title | Book title |
| price | Original book price |
| star_rating | Rating as text |
| availability | Stock availability |
| category | Book category |

The dataset contains more than 60 books, satisfying the project requirement.

---

# Data Cleaning and Transformation

## Price Cleaning

Original format:

```text
£51.77
```

Transformation:

```python
price_gbp = 51.77
```

The currency symbol was removed and values were converted to floating-point numbers.

---

## Rating Conversion

Original ratings:

```text
One
Two
Three
Four
Five
```

Converted to:

```text
1
2
3
4
5
```

using a rating dictionary.

---

## Availability Conversion

Original:

```text
In stock
```

Transformed into:

```python
True
```

Resulting column:

```text
in_stock
```

Boolean values were used to represent availability.

---

# Missing Value Handling

The pipeline includes safeguards against parsing failures.

## Numeric Fields

For numeric parsing issues:

```python
pd.to_numeric(errors="coerce")
```

was used.

Missing values were replaced using median imputation:

```python
column.fillna(column.median())
```

### Justification

Median imputation preserves dataset size while minimizing the influence of outliers.

---

## Non-Numeric Fields

Rows missing critical identifiers such as:

- Title
- Category

were removed.

### Justification

Imputing categorical identifiers could introduce incorrect information into the dataset.

---

# Currency Conversion

## Fixed Conversion Rate

The project specification requires the following
#---------------------------------------------------------------------------------
# Titanic Analytics Pipeline
#---------------------------------------------------------------------------------
## Project Overview
#---------------------------------------------------------------------------------
This project implements a complete analytics and machine learning pipeline using the Titanic dataset from Seaborn. The workflow covers data profiling, cleaning, exploratory data analysis (EDA), visualization, predictive modeling, hyperparameter tuning, class imbalance handling, regression analysis, and model deployment.

The dataset was loaded only once using:

```python
sns.load_dataset('titanic')
```

Immediately after loading, it was saved as:

```python
df.to_csv("titanic.csv", index=False)
```

This CSV serves as the project's offline fallback dataset and is used throughout the entire workflow.

---

# Project Structure

```text
analytics/
│
├── 01_eda.ipynb
├── 02_modeling.ipynb
├── titanic.csv
├── best_pipeline.joblib
├── charts/
│   ├── age_hist.png
│   ├── fare_hist.png
│   ├── correlation_heatmap.png
│   ├── chart1_gender_survival.png
│   ├── chart2_class_survival.png
│   ├── chart3_fare_survival.png
│   └── chart4_age_fare_survival.png
│
└── README.md
```

---

# Installation

Install the required packages:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn imbalanced-learn joblib
```

---

# Running the Project

## Step 1: Run EDA

```bash
jupyter notebook 01_eda.ipynb
```

This notebook:

- Loads Titanic dataset
- Saves titanic.csv
- Performs profiling
- Handles missing values
- Generates charts
- Performs correlation analysis
- Applies exploratory standardization

---

## Step 2: Run Modeling

```bash
jupyter notebook 02_modeling.ipynb
```

This notebook:

- Reads titanic.csv
- Builds preprocessing pipeline
- Trains classification models
- Evaluates performance
- Performs imbalance experiments
- Tunes Random Forest
- Performs regression analysis
- Saves deployment pipeline

---

# Dataset Profile

## Dataset Shape

```text
Rows: 891
Columns: 15
```

## Profiling Commands

```python
df.info()
df.describe()
df.shape
```

---

# Missing Value Analysis

| Column | Missing % | Strategy |
|----------|----------|-