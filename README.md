# E-Commerce Marketplace BI Dashboard – Power BI & Python Project


## Introduction

This **E-Commerce Marketplace BI Dashboard** was developed to analyze **marketplace revenue, order volume, product category performance, delivery operations, customer satisfaction, and seller performance** using the Olist Brazilian e-commerce dataset.

The project combines **Python/Pandas data preparation** with an interactive **Power BI report**. Nine raw marketplace CSV files were cleaned, transformed, validated, and merged into a dashboard-ready order-item dataset containing **112,650 records**.

The Power BI report contains **five analytical pages**, each designed to answer a specific business question and provide an executive-friendly view of marketplace performance.

---

## Power BI Dashboard

The complete interactive Power BI report is available here:

[project_1_bi_dashboard.pbix](./project_1_bi_dashboard.pbix)

---

## Python Data Preparation

The dashboard dataset was created using Python and Pandas.

- [Python notebook walkthrough](./01_create_dashboard_orders_summary.ipynb)
- [Python script](./01_create_dashboard_orders_summary.py)

### Data Preparation Workflow

1. Loaded and profiled nine raw Olist CSV files.
2. Checked data types, record counts, and missing values.
3. Converted order timestamp fields from text to datetime.
4. Aggregated payment and review records to the order level before merging.
5. Translated product categories from Portuguese to English.
6. Merged order items with orders, customers, products, sellers, payments, and reviews.
7. Created delivery, revenue, and time-based fields for reporting.
8. Validated the final dataset for duplicate order items, missing IDs, negative values, and invalid records.
9. Exported a dashboard-ready dataset for Power BI.

---

## Power BI Skills Used

- **📊 Interactive Dashboard Design & Business Storytelling**
- **🧮 DAX Measures and Calculated Columns**
- **🐍 Python Data Cleaning and Transformation**
- **🧹 Data Quality Validation**
- **📈 KPI Development**
- **🎨 Conditional Formatting and Gradient Ranking Visuals**
- **📦 Marketplace, Category, Delivery, and Seller Analysis**

---

## Dataset

This project uses the **Olist Brazilian E-Commerce Dataset**, a public marketplace dataset containing customer, order, seller, product, payment, review, and delivery information.

Key attributes include:

- **🛒 Orders, Order Items, and Order Status**
- **💰 Product Price, Freight Value, and Payment Value**
- **👥 Customers and Customer Location**
- **🏪 Sellers and Seller Location**
- **📦 Product Categories**
- **⭐ Customer Review Scores**
- **🚚 Actual and Estimated Delivery Dates**
- **📅 Purchase Dates and Monthly Trends**

---

## Dashboard Breakdown

### 📊 Dashboard 1: Executive Overview

<img width="1490" height="836" alt="image" src="https://github.com/user-attachments/assets/f4f324fb-8a09-489e-a37f-7e64e9053c2a" />

**Business Questions:**  
*How is the marketplace performing overall across revenue, orders, customer experience, and regional demand?*

#### Visualizations Included

- **KPI Cards:** Revenue, total orders, average order value, average review score, late delivery rate, and total customers
- **Monthly Revenue Trend:** Revenue performance over time
- **Top Product Categories by Revenue:** Highest-revenue product categories
- **Top Customer States by Orders:** States contributing the most marketplace orders

📌 **Key Insight:**  
The marketplace generated **15.85M in revenue** across **98,666 orders** from **95,420 customers**, while maintaining an overall **4.03 average review score** and a **7.93% late delivery rate**.

---

### 📦 Dashboard 2: Product & Category Analysis

<img width="1494" height="837" alt="image" src="https://github.com/user-attachments/assets/c00e5348-5473-4990-ac5d-fc150870343a" />

**Business Questions:**  
*Which high-volume product categories drive order volume, freight cost, customer satisfaction, and delivery risk?*

#### Visualizations Included

- **Top 10 Categories by Order Volume**
- **Average Review Score for High-Volume Categories**
- **Average Freight Value for High-Volume Categories**
- **Late Delivery Rate for High-Volume Categories**
- **Category KPI Cards:** Category count, items sold, average freight value, average review score, and late delivery orders

📌 **Key Insight:**  
Category performance varies beyond order volume: high-volume categories can differ substantially in average freight cost, review scores, and late-delivery exposure. This view helps identify categories that require operational attention rather than focusing only on sales.

---

### 📋 Dashboard 3: Category Details

<img width="1492" height="839" alt="image" src="https://github.com/user-attachments/assets/6149fa7f-9eba-4196-beb2-6ab0530f1cc5" />

**Business Questions:**  
*What are the exact category-level metrics behind the dashboard rankings?*

#### Visualizations Included

- **Category Details Table:** Revenue, orders, average order value, review score, late delivery rate, average freight value, and average delivery days
- **Conditional Formatting:** Highlights elevated late-delivery risk and lower customer review scores

📌 **Key Insight:**  
The detailed table enables comparison of commercial performance and customer experience metrics in one view, making it easier to identify categories with strong sales but potential freight, delivery, or satisfaction issues.

---

### 🚚 Dashboard 4: Delivery & Customer Experience

<img width="1496" height="839" alt="image" src="https://github.com/user-attachments/assets/573998ff-c877-4467-9f66-058b15aed7ae" />

**Business Questions:**  
*How do delivery performance and regional delivery risk affect customer satisfaction?*

#### Visualizations Included

- **On-Time vs Late Delivery Review Score Comparison**
- **Monthly Late Delivery Rate Trend**
- **Late Delivery Rate by High-Volume Customer State**
- **Longest Average Delivery Time by High-Volume Customer State**
- **KPI Cards:** Late delivery rate, late delivery orders, average delivery days, and average review score

📌 **Key Insight:**  
Late deliveries were strongly associated with lower customer satisfaction: the average review score declined from **4.21 for on-time deliveries** to **2.55 for late deliveries**. This indicates that delivery reliability is a major driver of customer experience.

---

### 🏪 Dashboard 5: Seller Performance

<img width="1493" height="840" alt="image" src="https://github.com/user-attachments/assets/94b8743b-a39c-4fcf-a3dd-a51204a5be0d" />

**Business Questions:**  
*Which sellers drive marketplace performance, and where are seller-related delivery or review risks concentrated?*

#### Visualizations Included

- **Top 10 Sellers by Revenue**
- **Top 10 Sellers by Order Volume**
- **Late Delivery Rate by High-Volume Seller State**
- **Lowest Review Score by High-Volume Seller State**
- **KPI Cards:** Total sellers, revenue, total orders, late delivery rate, and average review score

📌 **Key Insight:**  
Seller performance is not defined only by revenue or order volume. The dashboard compares seller states across late delivery risk and customer review performance to identify potential operational quality gaps.

---

## Key Business Questions Answered

- How is marketplace revenue trending over time?
- Which product categories generate the most revenue and order volume?
- Which customer states contribute the most orders?
- How do late deliveries affect customer review scores?
- Which customer states face the highest delivery risk or longest delivery times?
- Which seller states demonstrate delivery or review performance concerns?
- Which categories combine high volume with elevated freight, delivery, or satisfaction risk?

---

## Key Project Results

- Processed **9 raw CSV files** into a validated reporting dataset with **112,650 order-item records**.
- Built a **five-page Power BI report** spanning executive KPIs, product analysis, delivery experience, category detail, and seller performance.
- Measured **15.85M revenue**, **98,666 orders**, **160.61 average order value**, **95,420 customers**, and **3,095 sellers**.
- Identified a **7.93% late delivery rate** across marketplace orders.
- Quantified the customer experience impact of late deliveries: **4.21 average review score for on-time deliveries vs 2.55 for late deliveries**.
- Used conditional formatting and gradient visuals to surface higher delivery risk and lower customer satisfaction across categories and seller/customer states.

---

## Conclusion

This project demonstrates an end-to-end business intelligence workflow: transforming raw marketplace data with Python, validating reporting data quality, creating DAX measures in Power BI, and presenting findings through an executive-ready dashboard.

It highlights the ability to connect revenue, product performance, operational delivery metrics, customer satisfaction, and seller performance into clear, actionable business insights.
