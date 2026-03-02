# Data Engineering Zoomcamp 2026 – dlt Homework: Build Your Own Taxi API Pipeline 

This repository contains my solution for the **dlt custom pipeline homework** of the [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp) (2026 cohort) Workshop, where I built a REST API ingestion pipeline for NYC Yellow Taxi data and loaded it into **DuckDB**.


## Assignment Overview

In this homework, we:

-Built a custom dlt REST API source (no scaffold provided)
-Implemented pagination logic (1,000 records per page) for 10 pages
-Loaded paginated JSON into DuckDB
-Explored the pipeline using:
    -dlt pipeline taxi_pipeline show
    -MCP Server queries
    -SQL queries
-Computed dataset insights from the loaded data

After setup, the pipeline processes NYC Taxi data and builds a dashboard of ingestion to final reporting tables

## Data Source


- **Base URL**: [NYC TLC Taxi Data](https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api)
- **Format**: Paginated JSON
- **Page Size**: 1,000 records
- **Destination**: DuckDB
- **Pagination Rule**: Stop when an empty page is returned or stop ater 10 pages
- - **Pipeline Nam**: taxi_pipeline

> _Screenshot proof below:_

![Data_tripdata](https://github.com/favhenry/docker-workshop-2026/blob/main/04-Analytics%20Engineering/images/Module%205%20Successful%20run%20diagram.PNG)
![Data_tripdata](https://github.com/favhenry/docker-workshop-2026/blob/main/04-Analytics%20Engineering/images/Module%205%20lineage%20diagram.PNG)



## 1. Question 1 Dataset Date Range

**Question:**  
What is the start date and end date of the dataset?

**Correct Answer:**  
 **✅ 2009-06-01 to 2009-07-01**

**Explanation:**  
After loading the dataset, querying the minimum and maximum pickup dates shows:


```sql
SELECT 
    MIN(tpep_pickup_datetime),
    MAX(tpep_pickup_datetime)
FROM taxi_data;
``` 

---

## 2. Question 2: Proportion of Credit Card Trips

**Question:**  
What proportion of trips are paid with credit card?

**Correct Answer:**  
✅ **26.66%**

**Explanation:**  
Using payment type analysis:

```sql
SELECT 
    ROUND(
        100.0 * SUM(CASE WHEN payment_type = 1 THEN 1 ELSE 0 END) 
        / COUNT(*), 
        2
    ) AS credit_card_percentage
FROM taxi_data;
``` 
---

## 3. Question 3. Total Tips Generated

**Question:**  
What is the total amount of money generated in tips?

**Correct Answer:**  
✅ **$6,063.41**

**Explanation:**  

```sql
SELECT ROUND(SUM(tip_amount), 2)
FROM taxi_data;
``` 

---

