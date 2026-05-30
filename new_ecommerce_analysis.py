import os
import csv
from collections import defaultdict
import matplotlib.pyplot as plt

#trying to find a CSV file with 'data' in its name
workspace_files = os.listdir('.')
file_path = None

for i in workspace_files:
    if i.lower().endswith('.csv') and 'data' in i.lower():
        file_path = i
        break

if not file_path:
    file_path = 'data.csv.csv' 

# Core KPI Counters
total_revenue = 0.0
successful_orders = set()

# Aggregation dictionaries ma
product_revenue = defaultdict(float)
country_revenue = defaultdict(float)
monthly_revenue = defaultdict(float)

print(f"Reading from data file: '{file_path}'...")

try:
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
                
                # Cleaning filters (skip returns/cancellations)
                if quantity > 0 and unit_price > 0 and description and not invoice_no.startswith('C'):
                    revenue = quantity * unit_price
                    
                    total_revenue += revenue
                    successful_orders.add(invoice_no)
                    product_revenue[description] += revenue
                    country_revenue[country] += revenue
                    
                    # Extract Year-Month
                    date_part = invoice_date.split()[0]
                    parts = date_part.split('/')
                    if len(parts) == 3:
                        ym = f"{parts[2]}-{parts[0].zfill(2)}"
                        monthly_revenue[ym] += revenue
            except (ValueError, IndexError):
                continue

    # Print Report to Terminal
    print("\n" + "="*55)
    print("🚀 INTERNSHIP TASK 1: SALES PERFORMANCE ANALYTICS REPORT")
    print("="*55)
    print(f"\n[1] CORE FINANCIAL METRICS:")
    print(f"    - Total Generated Revenue:  ${total_revenue:,.2f}")
    print(f"    - Total Successful Orders: {len(successful_orders):,}")

 #creating grapgh for top 5 products and monthly revenue trends

    print("\n Creating required data visualizations...")

    # Chart 1: Top 5 Products Bar Chart
    sorted_products = sorted(product_revenue.items(), key=lambda x: x[1], reverse=True)[:5]
    products = [p[0][:20] + '...' if len(p[0]) > 20 else p[0] for p in sorted_products] # shorten labels
    prod_revenues = [p[1] for p in sorted_products]

    plt.figure(figsize=(10, 5))
    plt.bar(products, prod_revenues, color='skyblue', edgecolor='black')
    plt.title('Top 5 Products by Revenue', fontsize=14, fontweight='bold')
    plt.xlabel('Product Description', fontsize=12)
    plt.ylabel('Revenue ($)', fontsize=12)
    plt.xticks(rotation=15, ha='right')
    plt.tight_layout()
    plt.savefig('top_products.png') # Saves chart as an image file
    plt.close()
    print("    Created 'top_products.png'")

    # Chart 2: Monthly Revenue Trends Line Graph
    sorted_months = sorted(monthly_revenue.items())
    months = [m[0] for m in sorted_months]
    month_revenues = [m[1] for m in sorted_months]

    plt.figure(figsize=(11,5))
    plt.plot(months, month_revenues, marker='o', color='darkgreen', linewidth=2)
    plt.title('Monthly Sales Revenue Trends (Seasonality)', fontsize=14, fontweight='bold')
    plt.xlabel('Timeline (Year-Month)', fontsize=12)
    plt.ylabel('Revenue ($)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig('monthly_trends.png') # Saves chart as an image file
    plt.close()
    print("    Created 'monthly_trends.png'")
    
    print("\n Visualizations saved directly to your workspace folder! You can insert them into your submission document.")

except FileNotFoundError:
    print(f"\n Missing file error.")