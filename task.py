import pandas as pd
import numpy as np

# 1. Load the CSV files
sales = pd.read_csv('raport_kwartalny_sprzedaz.csv')
catalog = pd.read_csv('katalog_produktow.csv')

# 2. Rename columns so they match for merging
sales.rename(columns={'ID_Produktu_Sprzedaz': 'product_id'}, inplace=True)
catalog.rename(columns={'ID_Produktu_Katalog': 'product_id'}, inplace=True)

# 3. Merge both datasets on "product_id"
merged = sales.merge(catalog, on='product_id', how='left', indicator=True)

# --- Task 1 ---
# Find sales that have no matching product in the catalog
missing_products = merged[merged['_merge'] == 'left_only']
unique_missing_products = missing_products['product_id'].nunique()
print("1. Unikalne ID produktu bez dopasowania:", unique_missing_products)


# --- Task 2 ---
# Calculate total sales value only for matched products
matched = merged[merged['_merge'] == 'both']
total_sales_value = matched['Wartosc_Sprzedazy'].sum()
print("2. Total sales value (matched products):", round(total_sales_value, 2))

# --- Task 3 ---
# Average unit price from sales for each product
avg_prices = matched.groupby('product_id')['Cena_Jednostkowa_Transakcji'].mean().reset_index()

# Add product name and catalog price from catalog
avg_prices = avg_prices.merge(catalog[['product_id', 'Nazwa_Produktu', 'Cena_Katalogowa']],
                              on='product_id')

# Calculate percentage difference between average sales price and catalog price
avg_prices['price_diff_percent'] = ((avg_prices['Cena_Jednostkowa_Transakcji'] - avg_prices['Cena_Katalogowa'])
                                    / avg_prices['Cena_Katalogowa']) * 100

# Find product with the biggest absolute difference
max_diff = avg_prices.loc[avg_prices['price_diff_percent'].abs().idxmax()]
print("3a. Product name:", max_diff['Nazwa_Produktu'])
print("3b. Price difference: {:+.2f}%".format(max_diff['price_diff_percent']))

# --- Task 4 ---
# Calculate value as quantity × unit price
sales['calculated_value'] = sales['Ilosc_Sprzedana'] * sales['Cena_Jednostkowa_Transakcji']

# Round both values to 2 decimal places
sales['Sales_Value_Rounded'] = sales['Wartosc_Sprzedazy'].round(2)
sales['Calculated_Value_Rounded'] = sales['calculated_value'].round(2)

# Check where values differ
sales['mismatch'] = sales['Sales_Value_Rounded'] != sales['Calculated_Value_Rounded']

# Count rows with mismatch
mismatch_count = sales['mismatch'].sum()

print("4. Number of rows with mismatch:", int(mismatch_count))

# --- Task 5 ---
if mismatch_count == 0:
    print("5a. No mismatches found")
else:
    print("5a. B")
    print("5b. The calculated value (quantity × unit price) is more reliable, "
          "because it comes directly from the raw transaction data, "
          "while reported values may have rounding or manual entry errors.")