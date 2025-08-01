## Description

This Python script performs a short sales data analysis based on two CSV files: a quarterly sales report and a product catalog.  

The analysis includes:

### 1. Data Loading & Merging
- Loads CSV files containing sales and product catalog data.  
- Standardizes column names and merges datasets by product ID.  

### 2. Missing Products Detection
- Identifies sales entries for products not listed in the catalog.  

### 3. Sales Value Analysis
- Calculates the total sales value only for products found in the catalog.  

### 4. Price Comparison
- Computes the average sales unit price for each product.  
- Compares average sales prices with catalog prices and finds the product with the largest percentage difference.  

### 5. Data Consistency Check
- Verifies if reported sales values match the product of quantity × unit price.  
- Counts mismatches and provides insight into the more reliable source of data.  

---

## Requirements
- Python 3.x  
- Libraries: `pandas`, `numpy`  

---

## Run
```bash
python task.py
