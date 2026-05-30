import os
import csv
from collections import defaultdict
import matplotlib.pyplot as plt

# looking for the data file in the sidebar folder
workspace_files = os.listdir('.')
file_path = None

for f in workspace_files:
    if f.lower().endswith('.csv') and 'data' in f.lower():
        file_path = f
        break

if not file_path:
    file_path = 'data.csv.csv'

total_revenue = 0.0
successful_orders = set()

# setup tracking dictionaries
product_revenue = defaultdict(float)
country_revenue = defaultdict(float)
monthly_revenue = defaultdict(float)

print(f"reading data file: '{file_path}'...")

# open the file and read rows
with open(file_path, mode='r', encoding='latin-1') as f:
    reader = csv.reader(f)
    headers = next(reader)
    
    for row in reader:
        if not row or len(row) < 8:
            continue
            
        try:
            invoice_no = row[0].strip()
            description = row[2].strip()
            quantity = int(row[3])
            invoice_date = row[4].strip()
            unit_price = float(row[5])
            country = row[7].strip()
            
            # data cleaning filters to remove cancellations
            if quantity > 0 and unit_price > 0 and description and not invoice_no.startswith('C'):
                revenue = quantity * unit_price
                
                total_revenue += revenue
                successful_orders.add(invoice_no)
                product_revenue[description] += revenue
                country_revenue[country] += revenue
                
                # get the year and month out of the date text
                date_part = invoice_date.split()[0]
                parts = date_part.split('/')
                if len(parts) == 3:
                    ym = f"{parts[2]}-{parts[0].zfill(2)}"
                    monthly_revenue[ym] += revenue
        except (ValueError, IndexError):
            continue

# print results report to the terminal
print("\n" + "="*50)
print("task 1: sales performance report")
print("="*50)
print(f"total generated revenue: ${total_revenue:,.2f}")
print(f"total successful orders: {len(successful_orders):,}")

# generate charts for the word report
print("\ncreating data charts...")

# 1. create the top products bar chart
sorted_products = sorted(product_revenue.items(), key=lambda x: x[1], reverse=True)[:5]
products = [p[0][:20] + '...' if len(p[0]) > 20 else p[0] for p in sorted_products] 
prod_revenues = [p[1] for p in sorted_products]

plt.figure(figsize=(10,5))
plt.bar(products, prod_revenues, color='skyblue', edgecolor='black')
plt.title('top 5 products by revenue', fontsize=12)
plt.xlabel('product description', fontsize=10)
plt.ylabel('revenue ($)', fontsize=10)
plt.xticks(rotation=15, ha='right')
plt.tight_layout()
plt.savefig('top_products.png') 
plt.close()
print("  created top_products.png")

# 2. create the monthly trends line chart
sorted_months = sorted(monthly_revenue.items())
months = [m[0] for m in sorted_months]
month_revenues = [m[1] for m in sorted_months]

plt.figure(figsize=(11, 5))
plt.plot(months, month_revenues, marker='o', color='darkgreen', linewidth=2)
plt.title('monthly sales trends', fontsize=12)
plt.xlabel('year-month', fontsize=10)
plt.ylabel('revenue ($)', fontsize=10)
plt.grid(True, linestyle='--', alpha=0.5)
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig('monthly_trends.png') 
plt.close()
print("  created monthly_trends.png")

print("\nprocessing finished successfully!")
