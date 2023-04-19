# Sales Analysis Dashboard

This web app provides an interactive dashboard for visualizing sales data from January 2019 to January 2020. The dashboard allows users to explore various sales metrics and filter the data by month.

## Features

- Interactive Plotly graphs
- Ability to filter data by month
- Display the following metrics:
  - Number of orders each month
  - Revenue each month
  - Revenue by product each month
  - Orders and revenue by city and state (map visualization)
  - Units sold each month for each product
  - Percentage of product sales by revenue and quantity

## Installation

To run the Sales Analysis Dashboard locally, follow these steps:

1. Install the required Python libraries:

```bash
pip3 install dash==2.5.0
pip3 install dash-bootstrap-components==1.4.1
pip3 install pandas==1.5.2
pip3 install plotly==5.5.0
```

2. Clone the repository or download the source code:

```bash
git clone https://github.com/thoang02/Sales-analysis-visualization.git
```

3. Change to the project directory

4. Run the app

```bash
python3 vis-plotly.py
```

5. Open a web browser and navigate to http://127.0.0.1:8050/ to view the dashboard.

## Deployment

To deploy the Sales Analysis Dashboard on a web server, follow the https://dash.plotly.com/deployment guide.
