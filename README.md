# Enterprise Retail Intelligence Command Centre

## End-to-end retail analytics platform using Python, SQL Server, Power BI, Machine Learning and Docker

---

# Project Overview

This project simulates a real enterprise retail analytics system built from scratch using:
- Python ETL pipelines
- SQL Server Data Warehouse
- Star Schema Modeling
- Power BI Dashboards
- Machine Learning
- Forecasting
- Docker

The goal was to transform raw e-commerce CSV files into executive dashboards and predictive business insights.

---

# Business Problems Solved

The platform answers critical business questions like:

- How much revenue is the company generating?
- Which customers and cities drive the most revenue?
- Are deliveries getting slower over time?
- Which product categories perform best?
- What will future sales look like?

---

# Tech Stack

| Area | Technologies |
|---|---|
| Data Engineering | Python, Pandas |
| Database | SQL Server |
| Data Modeling | Star Schema |
| Analytics | SQL |
| BI & Reporting | Power BI, DAX |
| Machine Learning | Scikit-learn, Prophet |
| Automation | Airflow |
| DevOps | Docker |

---

# System Architecture

```text
CSV Files
   ↓
Python ETL Pipelines
   ↓
SQL Server Staging Tables
   ↓
Star Schema Data Warehouse
   ↓
Power BI Dashboards
   ↓
Machine Learning Models
   ↓
Forecasting & Predictions
```

---

# Dashboards Built

## 1. Executive Overview
- Revenue KPIs
- Revenue trends
- Geographic analysis
- Product category insights

![Executive Dashboard](images/dashboards/01_executive_overview.png)

---

## 2. Customer Analytics
- Customer distribution
- Top revenue cities
- Payment behavior
- Customer segmentation

![Customer Dashboard](images/dashboards/02_customer_analytics.png)

---

## 3. Logistics & Shipping
- Delivery performance
- Freight cost analysis
- Late delivery tracking
- Shipping efficiency metrics

![Logistics Dashboard](images/dashboards/03_logistics.png)

---

## 4. Product Intelligence
- Product profitability
- Category analysis
- Freight vs revenue analysis
- Treemap visualizations

![Product Dashboard](images/dashboards/04_product_intelligence.png)

---

## 5. Forecast & Predictive Analytics
- Revenue forecasting
- AI prediction intervals
- Seasonal trend analysis

![Forecast Dashboard](images/dashboards/05_forecast.png)

---

# Key Insights

- São Paulo generated the highest revenue concentration
- Health & Beauty became the top-performing category
- Delivery times increased as order volume scaled
- VIP customers contributed disproportionately to revenue
- Forecasting predicted strong seasonal revenue spikes

---

# Machine Learning Models

## Sales Forecasting
Used Facebook Prophet to predict future revenue trends.

## Customer Segmentation
Used K-Means clustering with RFM analysis to identify:
- VIP customers
- loyal customers
- churn-risk customers

## Churn Prediction
Built Random Forest models to identify customers likely to stop purchasing.

---

# Skills Demonstrated

- Python ETL Development
- SQL Analytics
- Star Schema Design
- Data Warehousing
- Power BI Dashboarding
- DAX Measures
- Machine Learning
- Forecasting
- Docker & Automation

---

# Repository Structure

```text
enterprise-retail-intelligence-platform/
│
├── dashboards/
├── images/
├── notebooks/
├── scripts/
├── sql/
├── utils/
├── airflow/
├── docker/
│
├── README.md
├── requirements.txt
├── docker-compose.yml
└── .gitignore
```

---

# About Me

I enjoy building complete analytics systems that solve real business problems using data engineering, analytics and machine learning.

---

# Connect With Me

| Platform | Link |
|---|---|
| LinkedIn | https://www.linkedin.com/in/yash-rathi0207/ |
| GitHub | https://github.com/YashRathi0206 |
| Email | yashrathi7658@gmail.com |

---

# Final Note

This project was built to simulate how modern companies build enterprise-grade analytics platforms for decision making, forecasting and operational intelligence.