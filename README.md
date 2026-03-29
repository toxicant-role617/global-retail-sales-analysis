# Global Retail Sales & Profit Analysis
**Power BI Dashboard Project | Microsoft Power BI Professional Certificate (Coursera)**

---

## What is this project?

This is my capstone project for the Microsoft Power BI Data Analyst Professional Certificate on Coursera. The dataset is based on a fictional retail company called Tailwind Traders that sells products in 5 countries — USA, UK, France, Australia, and UAE.

I built this project to practice everything I learned throughout the course — loading data, cleaning it, building a data model, writing DAX, and finally creating reports and a dashboard.

Honestly this took me longer than I expected, mostly because of some bugs I ran into (more on that below). But I think I learned more from fixing those bugs than from the actual lessons.

---

## What does the dashboard show?

I created two report pages:

**Sales Overview**
- Which country has the most loyal customers (by loyalty points)
- Which products sell the most by quantity
- How median sales are distributed across countries
- How median sales trend over time

**Profit Overview**
- Which products generate the highest net revenue
- What the yearly profit margin looks like by country
- How profit margin has changed over time

---

## Tools I used

- **Microsoft Excel** – to prepare the raw sales data before loading it into Power BI
- **Power BI Desktop** – main tool for building the data model and reports
- **Power Query** – for cleaning and transforming the data
- **DAX** – for creating calculated tables and measures
- **Python** – I used a small Python script to generate the currency exchange rate table (this was new to me)
- **Power BI Service** – to publish the report and create the executive dashboard

---

## Data sources

| File | What it contains |
|---|---|
| Tailwind-Traders-Sales.xlsx | 54 sales records with product, price, tax, quantity |
| Purchases.xlsx | 54 purchase records with dates, return status, warranty |
| Countries.xlsx | 5 country records linked to exchange rates |
| Currency data (Python script) | Exchange rates for USD, GBP, EUR, AED, AUD |

Before loading the sales file into Power BI, I added 3 columns in Excel:

```
Gross Revenue = Gross Product Price × Quantity Purchased
Total Tax     = Tax Per Product × Quantity Purchased
Net Revenue   = Gross Revenue − Total Tax
```

---

## Data model

I used a snowflake schema. There are 6 tables connected with 5 relationships.

```
CalendarTable ──── Purchases ──── Sales ──── Countries ──── df (currency)
                                    │
                              Sales in USD
```

The `Sales in USD` table is a calculated DAX table that converts all revenue figures into USD using the exchange rates.

The `CalendarTable` is also created using DAX — it covers 2020 to 2023 and is used for time intelligence measures like YTD profit.

---

## DAX measures I wrote

```dax
-- Profit per order
Profit in USD = 'Sales in USD'[Net Revenue USD] - 'Sales in USD'[Total Tax USD]

-- Overall profit margin
Yearly Profit Margin = 
DIVIDE(
    SUM('Sales in USD'[Profit in USD]),
    SUM('Sales in USD'[Net Revenue USD])
)

-- Quarter to date profit
Quarterly Profit = 
CALCULATE(
    SUM('Sales in USD'[Profit in USD]),
    DATESQTD(CalendarTable[Date])
)

-- Year to date profit
YTD Profit = 
TOTALYTD(
    SUM('Sales in USD'[Profit in USD]),
    CalendarTable[Date]
)

-- Median of all sales values
Median Sales = MEDIAN('Sales in USD'[Gross Revenue USD])
```

---

## Key numbers from the dashboard

| Metric | Value |
|---|---|
| Median Sales | $222.50 |
| Yearly Profit Margin | 92.35% |
| YTD Profit | $9.06K |
| Net Revenue USD | $13.89K |
| Gross Revenue USD | $14.97K |
| Country with most loyalty points | UK (315) |
| Largest share of sales | USA (63.49%) |
| Highest net revenue product | Luminous Bulb 60W |

---

## Problems I ran into

I want to write these down because they took me a while to figure out and I do not want to forget them.

**1. Power BI could not find pandas**

When I tried to run the Python script inside Power BI, I kept getting a "no module named pandas" error even though I had already installed it. Turned out I had 3 different Python installations on my PC and Power BI was pointing to the wrong one. I ran `where python` in CMD to list all versions, then checked each one with `python.exe -m pip show pandas` to find which one actually had pandas. Then I updated the Python path in Power BI settings under File → Options → Python scripting.

**2. Exchange rates were 100x too high**

The Python script used commas as decimal separators like `0,75` for GBP but my system was reading those as whole numbers so it became `75` instead of `0.75`. All the UK and France sales were inflated by 100 times because of this. I only noticed because the Median Sales card was showing $6,380 instead of what I expected. Fixed it by replacing all the commas with dots in the script.

**3. RELATED() was not working in the DAX table**

When I was writing the `Sales in USD` calculated table, I used `RELATED()` to pull the exchange rate but kept getting an error about multiple columns. The problem was that the currency table was not directly connected to Sales — it went through the Countries table in between. I had to switch to `LOOKUPVALUE()` which can find a value in any table directly without needing the relationship chain.

**4. Calendar table was linked to the wrong column**

I accidentally linked the CalendarTable to `Purchases[PurchaseID]` instead of `Purchases[Purchase Date]`. Because of this the relationship was marked as inactive and my YTD and QTD measures were returning blank. Took me a while to spot it in the Manage Relationships screen.

---

## What I learned

- Data preparation matters more than I thought. The decimal separator bug caused me to get completely wrong numbers and I only caught it by accident.
- `RELATED()` only works when there is a direct active relationship between two tables. If the path goes through a third table you need `LOOKUPVALUE()` instead.
- Time intelligence functions like `TOTALYTD` and `DATESQTD` will not work unless you have a proper Calendar table connected correctly.
- In Power BI Service, dashboards and reports are two different things. You build the report in Desktop and then pin individual visuals to a dashboard in the browser.
- The Performance Analyzer in Power BI shows how long each visual takes to load. All my DAX measures ran under 200ms which is the recommended limit.

---

## How to open this project

1. Download the files from the `data/` folder
2. Open **Power BI Desktop**
3. Load each Excel file via Get Data → Excel Workbook
4. Load the currency data via Get Data → Python Script and paste the script from `assets/currency-script.py`
5. Recreate the relationships shown in the data model section
6. Add the DAX measures using the code above

---

## Files in this repo

```
global-retail-sales-analysis/
│
├── README.md
├── .gitignore
│
├── data/
│   ├── Tailwind-Traders-Sales.xlsx
│   ├── Purchases.xlsx
│   └── Countries.xlsx
│
├── report/
│   ├── Tailwind Traders Report.pbix
│   └── Global-Retail-Sales-Report.pdf
│
├── assets/
│   └── currency-script.py
│
└── screenshots/
    └── dashboard.png
```

---

## About me

I am a technical trainer currently completing my MSc in Computer Science. I am working on transitioning into data analytics and data science and building my portfolio through hands-on projects like this one.

- [LinkedIn](https://www.linkedin.com/in/your-profile)
- [GitHub](https://github.com/mitadrudeb)

---

*This project was completed as part of the Microsoft Power BI Data Analyst Professional Certificate on Coursera. The data used is fictional and provided for educational purposes only.*
