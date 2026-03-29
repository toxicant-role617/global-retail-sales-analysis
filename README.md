# Global Retail Sales & Profit Analysis
**An end-to-end business intelligence project built with Microsoft Power BI**

---

## Overview

This project analyzes the sales and profit performance of a global retail business operating across five countries — USA, UK, France, Australia, and UAE. The goal was to build a complete BI solution that gives a clear picture of where revenue is coming from, which products are performing well, and how profit margins are holding up over time.

The analysis covers data preparation, data modeling, DAX calculations, interactive reporting, and an executive dashboard — all in a single Power BI solution.

---

## Business Questions

- Which countries generate the most customer loyalty?
- Which products sell the most by quantity?
- What is the net revenue breakdown by product?
- How does profit margin trend over time and across countries?
- What do total sales and profits look like when normalized to a single currency (USD)?

---

## Tools & Technologies

| Tool | Purpose |
|---|---|
| Microsoft Excel | Raw data preparation and calculated columns |
| Power BI Desktop | Data modeling, DAX measures, report design |
| Power Query | Data transformation and cleaning |
| DAX | Calculated tables, measures, time intelligence |
| Python (pandas) | Generating structured currency exchange data |
| Power BI Service | Publishing, executive dashboard, alerts, subscriptions |

---

## Data Sources

| Table | Source | Records | Description |
|---|---|---|---|
| Sales | Excel | 54 | Product sales with price, quantity, and tax |
| Purchases | Excel | 54 | Purchase records filtered to non-returned orders |
| Countries | Excel | 5 | Country lookup table with exchange rate mapping |
| Currency | Python Script | 5 | Exchange rates for USD, GBP, EUR, AED, AUD |

### Data Preparation

Before loading into Power BI, three calculated columns were added to the Sales file in Excel:

```
Gross Revenue = Gross Product Price × Quantity Purchased
Total Tax     = Tax Per Product × Quantity Purchased
Net Revenue   = Gross Revenue − Total Tax
```

Purchases data was filtered to exclude returned orders, keeping only valid completed transactions.

---

## Data Model

The model follows a **Snowflake Schema** with 6 tables and 5 active relationships.

```
CalendarTable ──── Purchases ──── Sales ──── Countries ──── df (currency)
                                    │
                              Sales in USD
```

**Relationships:**

| From | To | Field | Cardinality | Filter Direction |
|---|---|---|---|---|
| Purchases | CalendarTable | Purchase Date → Date | Many:1 | Both |
| Purchases | Sales | OrderID | 1:1 | Both |
| Sales | Countries | Country ID | Many:1 | Both |
| Countries | df | Exchange ID | 1:1 | Both |
| Sales in USD | Sales | OrderID | Many:1 | Both |

**CalendarTable** was created using DAX to enable time intelligence:

```dax
CalendarTable = 
ADDCOLUMNS(
    CALENDAR(DATE(2020, 1, 1), DATE(2023, 12, 31)),
    "Year", YEAR([Date]),
    "Month Number", MONTH([Date]),
    "Month", FORMAT([Date], "MMMM"),
    "Quarter", QUARTER([Date]),
    "Weekday", WEEKDAY([Date]),
    "Day", DAY([Date])
)
```

**Sales in USD** is a calculated table that converts all revenue figures to USD using live exchange rates:

```dax
Sales in USD = 
ADDCOLUMNS(
    Sales,
    "Country Name", RELATED(Countries[Country]),
    "Exchange Rate", LOOKUPVALUE('df'[ExchangeRate], 'df'[Exchange ID], 
                     RELATED(Countries[Exchange ID])),
    "Exchange Currency", LOOKUPVALUE('df'[Exchange Currency], 'df'[Exchange ID], 
                          RELATED(Countries[Exchange ID])),
    "Gross Revenue USD", [Gross Revenue] * LOOKUPVALUE('df'[ExchangeRate], 
                          'df'[Exchange ID], RELATED(Countries[Exchange ID])),
    "Net Revenue USD", [Net Revenue] * LOOKUPVALUE('df'[ExchangeRate], 
                        'df'[Exchange ID], RELATED(Countries[Exchange ID])),
    "Total Tax USD", [Total Tax] * LOOKUPVALUE('df'[ExchangeRate], 
                      'df'[Exchange ID], RELATED(Countries[Exchange ID]))
)
```

> Note: `LOOKUPVALUE()` was used instead of `RELATED()` here because the currency table does not have a direct relationship with the Sales table — the path goes through Countries as an intermediate table.

---

## DAX Measures

```dax
-- Base profit calculation
Profit in USD = 'Sales in USD'[Net Revenue USD] - 'Sales in USD'[Total Tax USD]

-- Profit as a percentage of net revenue
Yearly Profit Margin = 
DIVIDE(
    SUM('Sales in USD'[Profit in USD]),
    SUM('Sales in USD'[Net Revenue USD])
)

-- Cumulative profit for the current quarter
Quarterly Profit = 
CALCULATE(
    SUM('Sales in USD'[Profit in USD]),
    DATESQTD(CalendarTable[Date])
)

-- Running profit total from the start of the year
YTD Profit = 
TOTALYTD(
    SUM('Sales in USD'[Profit in USD]),
    CalendarTable[Date]
)

-- Middle value across all sales transactions
Median Sales = MEDIAN('Sales in USD'[Gross Revenue USD])
```

---

## Report Pages

### Sales Overview

| Visual | Type |
|---|---|
| Loyalty Points by Country | Horizontal Bar Chart |
| Quantity Sold by Product | Column Chart |
| Median Sales Distribution by Country | Pie Chart |
| Median Sales Over Time | Line Chart with Trend Line |
| Stock, Quantity Purchased, Median Sales | Cards |
| Country Name | Slicer |

### Profit Overview

| Visual | Type |
|---|---|
| Net Revenue by Product | Horizontal Bar Chart |
| Yearly Profit Margin by Country | Donut Chart |
| Yearly Profit Margin Over Time | Area Chart |
| YTD Profit, Net Revenue USD | Cards |
| Gross Revenue USD | KPI Visual |
| Date Range | Slicer |

---

## Key Results

| Metric | Value |
|---|---|
| Median Sales (USD) | $222.50 |
| Yearly Profit Margin | 92.35% |
| YTD Profit | $9.06K |
| Net Revenue USD | $13.89K |
| Gross Revenue USD | $14.97K |
| Highest Loyalty Points | UK — 315 |
| Largest Sales Share by Country | USA — 63.49% |
| Highest Net Revenue Product | Luminous Bulb 60W |

---

## Challenges & Solutions

**Python path mismatch**
Power BI was unable to locate `pandas` despite it being installed. The system had three separate Python installations and Power BI was pointing to the wrong one. Resolved by identifying the correct installation using `where python` in CMD, verifying which had pandas with `pip show pandas`, and updating the path in Power BI Options.

**Decimal separator issue in exchange rates**
The currency script used commas as decimal separators (`0,75`) which the system interpreted as whole numbers (`75`). This caused exchange rates to be inflated 100x, making median sales appear as $6,380 instead of $222.50. Fixed by replacing commas with dots in the script.

**Multi-hop relationship in DAX**
`RELATED()` failed when pulling exchange rates from the currency table because the relationship path passed through an intermediate table (Countries). Resolved by switching to `LOOKUPVALUE()` which retrieves values directly from any table without requiring a relationship chain.

**Inactive calendar relationship**
The CalendarTable was linked to `Purchases[PurchaseID]` instead of `Purchases[Purchase Date]`, causing the relationship to be marked inactive. Time intelligence measures returned blank until the relationship was corrected.

---

## Project Structure

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
    └── dashboard.jpg
```

---

## How to Run

1. Clone the repository
2. Open **Power BI Desktop** and load the three Excel files from `data/` via Get Data → Excel Workbook
3. Load the currency exchange data via Get Data → Python Script using the script in `assets/currency-script.py`
4. Recreate the table relationships as documented in the Data Model section
5. Add the DAX measures from the code blocks above
6. Build the report visuals as described in the Report Pages section

---

## Connect

- [LinkedIn](https://www.linkedin.com/in/your-profile)
- [GitHub](https://github.com/mitadrudeb)
