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
#--------------------------------------------------------------------------------
# Support Assistant Module
#--------------------------------------------------------------------------------
## Project Overview
#--------------------------------------------------------------------------------
This project implements a Retrieval-Augmented Generation (RAG) based customer support assistant for Zepto policies.

The assistant:

- Loads Zepto policy documents.
- Generates embeddings using Sentence Transformers.
- Stores embeddings in ChromaDB.
- Uses LangGraph for workflow orchestration.
- Uses FastAPI to expose an API endpoint.
- Returns structured JSON responses validated by Pydantic.
- Supports a deterministic offline mock mode through the `MOCK_LLM` flag.

The graded implementation runs completely offline without requiring:

- API keys
- LLM subscriptions
- Internet connectivity

---

# Project Structure

```text
support_assistant/
│
├── docs/
│   ├── doc_01.txt
│   ├── doc_02.txt
│   ├── doc_03.txt
│   ├── doc_04.txt
│   ├── doc_05.txt
│   ├── doc_06.txt
│   ├── doc_07.txt
│   └── doc_08.txt
│
├── main.py
├── requirements.txt
├── Dockerfile
├── README.md
└── chroma_db/
```

---

# Technologies Used

- Python
- FastAPI
- LangGraph
- ChromaDB
- Sentence Transformers
- Pydantic
- Docker

---

# Installation

Install all dependencies:

```bash
pip install -r requirements.txt
```

---

# Environment Variable

The project supports two modes:

## Mock Mode (Default)

```bash
MOCK_LLM=1
```

or leave it unset.

No LLM API call is made.

This is the required graded implementation.

---

## Optional Real LLM Mode

```bash
MOCK_LLM=0
```

In this mode a real LLM provider can be integrated.

This feature was not required for grading.

---

# Document Corpus

The assistant uses 8 Zepto policy documents:

| Document | Topic |
|----------|----------|
| doc_01 | Delivery Policy |
| doc_02 | Returns & Refunds |
| doc_03 | Membership Tiers |
| doc_04 | Order Tracking |
| doc_05 | Order Cancellation |
| doc_06 | Damaged/Missing Items |
| doc_07 | Gift Cards |
| doc_08 | Customer Support Hours |

---

# Embedding and Storage

The project uses:

```python
SentenceTransformer(
    "all-MiniLM-L6-v2"
)
```

for generating document embeddings.

Embeddings are stored in:

```text
ChromaDB Collection:
zepto_collection
```

The collection is persisted in:

```text
chroma_db/
```

---

# Prompt Template

The system uses a structured prompt format based on:

```text
ROLE
CONTEXT
TASK
FORMAT
LENGTH
```

Template:

```text
ROLE:
You are a Zepto customer support assistant.

CONTEXT:
{context}

TASK:
Answer the user's question using only the supplied context.

NEGATIVE CONSTRAINT:
Do not answer using information not present in the provided context.

FORMAT:
Provide a short factual answer.

LENGTH:
Maximum 100 words.

FEW SHOT EXAMPLE:

Question:
What is the refund timeline?

Answer:
Approved refunds are credited within 3–5 business days.

Question:
{query}

Answer:
```

---

# LangGraph Workflow

The assistant is implemented using a LangGraph StateGraph.

## State Definition

```python
class SupportState(TypedDict):

    query: str

    intent: str

    answer: str

    sources: list
```

---

## Node 1: classify_intent

Purpose:

Determine whether the user query requires policy retrieval.

### Mock Classification Rule

Keywords:

```text
delivery
return
refund
membership
tracking
cancel
gift card
support hours
```

If any keyword is detected:

```text
policy_question
```

Otherwise:

```text
general_question
```

---

## Node 2: retrieve_and_answer

Purpose:

Answer policy-related queries.

Actions:

1. Generate query embedding.
2. Retrieve top 3 chunks from ChromaDB.
3. Select most relevant chunk.
4. Produce response.

Mock response format:

```text
Based on the retrieved context:
{top_chunk_excerpt}
```

---

## Node 3: direct_answer

Purpose:

Handle non-policy queries.

Mock response:

```text
I can only answer questions about Zepto policies right now.
```

---

## Conditional Routing

The graph routes queries as follows:

```text
User Query
      ↓
classify_intent
      ↓
 ┌──────────────┐
 │ policy_question? │
 └──────┬───────┘
        │
   Yes  │  No
        │
        ↓

retrieve_and_answer

or

direct_answer
```

---

# JSON Output Schema

Every response follows this schema:

```json
{
  "answer": "string",
  "sources": ["doc_id"],
  "confidence": 1.0
}
```

---

## Fields

### answer

Generated response text.

---

### sources

List of source documents used.

Example:

```json
[
  "doc_02.txt"
]
```

General questions return:

```json
[]
```

---

### confidence

A confidence score between:

```text
0.0 and 1.0
```

Mock mode uses:

```json
1.0
```

---

# FastAPI Endpoint

## Endpoint

```http
POST /ask
```

### Request

```json
{
  "query": "What is the refund policy?"
}
```

---

### Response

```json
{
  "answer": "Based on the retrieved context: Grocery and perishable items may be reported for a return within 24 hours...",
  "sources": [
    "doc_02.txt"
  ],
  "confidence": 1.0
}
```

---

# Example Calls

## Example 1: Policy Question

### Request

```json
{
  "query": "What is the refund policy?"
}
```

### Response

```json
{
  "answer": "Based on the retrieved context: Grocery and perishable items may be reported for a return within 24 hours of delivery...",
  "sources": [
    "doc_02.txt"
  ],
  "confidence": 1.0
}
```

### Routing

```text
classify_intent
        ↓
policy_question
        ↓
retrieve_and_answer
```

---

## Example 2: General Question

### Request

```json
{
  "query": "Who won the cricket world cup?"
}
```

### Response

```json
{
  "answer": "I can only answer questions about Zepto policies right now.",
  "sources": [],
  "confidence": 1.0
}
```

### Routing

```text
classify_intent
        ↓
general_question
        ↓
direct_answer
```

---

# Architecture Description

The assistant follows a Retrieval-Augmented Generation (RAG) architecture.

---

## Stage 1: Ingestion

Component:

```text
main.py
```

Actions:

- Read all documents from `/docs`
- Load document content into memory

Output:

```text
Raw document text
```

---

## Stage 2: Embedding

Component:

```python
SentenceTransformer(
    "all-MiniLM-L6-v2"
)
```

Actions:

- Convert documents into vector embeddings

Output:

```text
Vector embeddings
```

---

## Stage 3: Storage

Component:

```text
ChromaDB
```

Collection:

```text
zepto_collection
```

Actions:

- Store embeddings
- Store document text
- Store document IDs

Output:

```text
Searchable vector database
```

---

## Stage 4: Retrieval

Component:

```text
retrieve_and_answer node
```

Actions:

- Embed user query
- Search ChromaDB
- Retrieve top 3 matching documents

Output:

```text
Relevant context chunks
```

---

## Stage 5: Generation

Components:

```text
retrieve_and_answer
direct_answer
```

Actions:

Generate final answer.

---

# MOCK_LLM Behavior

## MOCK_LLM = 1 (Default)

No LLM call.

Responses are generated using deterministic program logic.

### retrieve_and_answer

Returns:

```text
Based on the retrieved context:
...
```

### direct_answer

Returns:

```text
I can only answer questions about Zepto policies right now.
```

---

## MOCK_LLM = 0 (Optional)

Would allow integration with:

- Groq
- OpenAI
- Claude
- Any other free provider

This path was optional and not required for grading.

---

# Running Locally

Start the API:

```bash
python -m uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

Access Swagger UI to test the endpoint.

---

# Docker Support

## Build Image

```bash
docker build -t zepto-support .
```

---

## Run Container

```bash
docker run -p 7860:7860 zepto-support
```

---

## Access API

```text
http://localhost:7860/docs
```

---

# Deliverables

✅ 8 Zepto policy documents

✅ SentenceTransformer embeddings

✅ ChromaDB vector storage

✅ Structured prompt template

✅ LangGraph StateGraph

✅ Three required nodes

✅ Conditional routing

✅ Pydantic response schema

✅ FastAPI API

✅ Dockerfile

✅ Mock LLM implementation

✅ Retrieval-Augmented Generation workflow

✅ Example API calls

✅ Architecture documentation

---

# Conclusion

This project demonstrates a complete offline Retrieval-Augmented Generation (RAG) support assistant capable of answering Zepto policy questions using document retrieval, vector search, workflow orchestration, structured responses, and API deployment. The solution operates fully without external LLM dependencies and satisfies all required project specifications.