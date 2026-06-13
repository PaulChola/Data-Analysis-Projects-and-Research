#  Cyclistic Bike-Share Data Analysis (April 2020)

![Python](https://img.shields.io/badge/Python-Data%20Analysis-blue)
![Pandas](https://img.shields.io/badge/Pandas-EDA-yellow)
![Matplotlib](https://img.shields.io/badge/Visualization-Graphs-orange)
![Seaborn](https://img.shields.io/badge/Seaborn-Statistics-lightblue)

---

##  Project Overview

This project analyzes Cyclistic bike-share trip data for April 2020 to identify behavioral differences between **casual riders** and **annual members**.

The goal is to generate actionable insights that help improve marketing strategies and increase annual subscriptions.

---

##  Business Problem

Cyclistic wants to convert casual riders into annual members.  
This analysis answers:

- How do casual riders behave differently from members?
- When and how do each group use the bike system?
- What patterns can support marketing decisions?

---

##   Dataset

- Source: Divvy Bike Share Data
- Period: April 2020
- File: `202004-divvy-tripdata.csv`

---

##  Tools & Technologies

- Python 
- Pandas (data cleaning & transformation)
- Matplotlib (data visualization)
- Seaborn (statistical analysis)

---

##  Data Processing Workflow

1. Imported raw dataset using Pandas  
2. Converted timestamps to datetime format  
3. Created new features:
   - Ride duration (minutes)
   - Day of week
4. Removed invalid records (ride length ≤ 0)  
5. Grouped data by member type  
6. Generated summary statistics and visualizations  

---

##   Key Visualizations

### 🚲 Cyclistic Analysis Dashboard

![Cyclistic Analysis](https://github.com/PaulChola/Data-Analysis-Projects-and-Research/blob/main/Cyclistic_Project/outputs/visualizations/cyclistic_analysis.png)

This dashboard includes:

- Ride volume comparison (Members vs Casual)
- Average ride duration comparison
- Weekly usage patterns
- Daily ride distribution trends

---

##   Key Insights

### 1. Ride Duration
- Casual riders take significantly longer trips than members
- Members have shorter, consistent ride durations

### 2. Usage Behavior
- Members use bikes consistently across weekdays
- Casual riders peak on weekends (leisure usage)

### 3. Business Insight
- Members = commuters
- Casual riders = recreational users

---

## Business Recommendations

- Promote weekend membership plans for casual riders
- Offer discounted annual plans for frequent weekend users
- Target casual riders with commuting-focused campaigns
- Highlight cost savings of membership for frequent riders

---

##  Output Files

| File | Description |
|------|-------------|
| cleaned_data.csv | Processed dataset |
| member_statistics.csv | Summary statistics |
| daily_summary.csv | Daily aggregated trends |
| cyclistic_analysis.png | Full visualization dashboard |

---

##  How to Run This Project

```bash
pip install pandas matplotlib seaborn

python cyclistic_analysis.py
