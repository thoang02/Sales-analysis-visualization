import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc
import plotly.subplots as sp


# Read data
data = pd.read_csv('sales-data.csv')
data['Order Date'] = pd.to_datetime(data['Order Date'], format='%Y-%m-%d %H:%M:%S')
data['Month'] = data['Order Date'].dt.month
data['Year'] = data['Order Date'].dt.year
data['Revenue'] = data['Quantity Ordered'] * data['Price Each']
data['City'] = data['Purchase Address'].apply(lambda x: x.split(',')[1].strip())
data['State'] = data['Purchase Address'].apply(lambda x: x.split(',')[2].split(' ')[1])

# Initialize the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MATERIA])

# Define app layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H2('Sales Analysis', style={'marginTop': 20, 'marginBottom': 20}),
            html.P('Select the metrics to analyze:', style={'marginBottom': 5}),
            # Create dropdpwn to view type of chart
            dcc.Dropdown(
                id='metrics-dropdown',
                options=[
                    {'label': 'Number of Orders', 'value': 'orders'},
                    {'label': 'Revenue', 'value': 'revenue'},
                    {'label': 'Revenue by Product', 'value': 'revenue_by_product'},
                    {'label': 'Orders & Revenue by City & State', 'value': 'orders_revenue_by_city_state'},
                    {'label': 'Units Sold by Product', 'value': 'units_sold'},
                    {'label': 'Percentage of Product Sales', 'value': 'percentage_sales'},
                ],
                multi=True,
                value=['orders', 'revenue']
            ),
            html.P('Select the months to analyze:', style={'marginTop': 20, 'marginBottom': 5}),
            # Create check list to chose the period of time
            dcc.Checklist(
                id='months-years-checklist',
                options=[
                    {'label': 'January 2019', 'value': '1_2019'},
                    {'label': 'February 2019', 'value': '2_2019'},
                    {'label': 'March 2019', 'value': '3_2019'},
                    {'label': 'April 2019', 'value': '4_2019'},
                    {'label': 'May 2019', 'value': '5_2019'},
                    {'label': 'June 2019', 'value': '6_2019'},
                    {'label': 'July 2019', 'value': '7_2019'},
                    {'label': 'August 2019', 'value': '8_2019'},
                    {'label': 'September 2019', 'value': '9_2019'},
                    {'label': 'October 2019', 'value': '10_2019'},
                    {'label': 'November 2019', 'value': '11_2019'},
                    {'label': 'December 2019', 'value': '12_2019'},
                    {'label': 'January 2020', 'value': '1_2020'}
                ],
                value=['1_2019', '2_2019', '3_2019', '4_2019', '5_2019', '6_2019', '7_2019', '8_2019', '9_2019', '10_2019', '11_2019', '1_2019']
            ),
        ], width=4),
        dbc.Col([
            html.Div(id='graphs-container', style={'marginTop': 20})
        ], width=8)
        ], style={'marginTop': 20})
        ], fluid=True)

# Define callbacks
@app.callback(
    Output('graphs-container', 'children'),
    Input('metrics-dropdown', 'value'),
    Input('months-years-checklist', 'value')
)
def update_graphs(selected_metrics, selected_months_years):
    graphs = []
    print('Selected metrics:', selected_metrics)
    print('Selected months years:', selected_months_years)

     # Split the selected month-year values into month and year components
    selected_months = [int(my.split('_')[0]) for my in selected_months_years]
    selected_years = [int(my.split('_')[1]) for my in selected_months_years]

    # Filter data by selected months
    data_filtered = data[(data['Month'].isin(selected_months)) & (data['Year'].isin(selected_years))]
    print('Filtered data:')
    print(data_filtered)
    
    # if 'orders' in selected_metrics:
    #     df_orders = data_filtered.groupby(['Year', 'Month']).size().reset_index(name='Orders')
    #     fig_orders = px.line(df_orders, x='Month', y='Orders', title='Number of Orders per Month')
    #     graphs.append(dcc.Graph(id='orders-graph', figure=fig_orders))

    # if 'revenue' in selected_metrics:
    #     df_revenue = data_filtered.groupby(['Year', 'Month'])['Revenue'].sum().reset_index()
    #     fig_revenue = px.line(df_revenue, x='Month', y='Revenue', title='Monthly Revenue')
    #     graphs.append(dcc.Graph(id='revenue-graph', figure=fig_revenue))
    
    # Show bar and line chart for monthly sales quantity and revenue
    if 'orders' in selected_metrics and 'revenue' in selected_metrics:
        df_orders_revenue = data_filtered.groupby(['Year', 'Month']).agg({'Revenue': 'sum', 'Order ID': 'count'}).reset_index()
        fig_orders_revenue = sp.make_subplots(specs=[[{"secondary_y": True}]])
        fig_orders_revenue.add_trace(go.Bar(x=df_orders_revenue['Month'], y=df_orders_revenue['Order ID'], name='Number of Orders'), secondary_y=False)
        fig_orders_revenue.add_trace(go.Scatter(x=df_orders_revenue['Month'], y=df_orders_revenue['Revenue'], name='Monthly Revenue'), secondary_y=True)
        fig_orders_revenue.update_layout(title='Number of Orders and Revenue per Month', xaxis_title='Month', yaxis_title='Number of Orders', yaxis2_title='Monthly Revenue')
        graphs.append(dcc.Graph(id='orders-revenue-graph', figure=fig_orders_revenue))

    # Show chart for revenue by product
    if 'revenue_by_product' in selected_metrics:
        df_revenue_by_product = data_filtered.groupby(['Year', 'Month', 'Product'])['Revenue'].sum().reset_index()
        fig_revenue_by_product = px.line(df_revenue_by_product, x='Month', y='Revenue', color='Product', title='Monthly Revenue by Product')
        graphs.append(dcc.Graph(id='revenue-by-product-graph', figure=fig_revenue_by_product))

    # Show map for revenue by cities and states    
    if 'orders_revenue_by_city_state' in selected_metrics:
        df_orders_revenue_by_city_state = data_filtered.groupby(['Year', 'Month', 'City', 'State']).agg({'Revenue': 'sum', 'Order ID': 'count'}).reset_index()
        fig_orders_revenue_by_city_state = px.scatter_geo(df_orders_revenue_by_city_state, locations='State', locationmode='USA-states', color='Revenue', size='Order ID', hover_name='City', title='Orders & Revenue by City & State')
        graphs.append(dcc.Graph(id='orders-revenue-by-city-state-graph', figure=fig_orders_revenue_by_city_state))
    
    # Show sales quantity by product
    if 'units_sold' in selected_metrics:
        if len(selected_months_years) == 1:
            # Show a bar chart when only one month is selected
            df_units_sold = data_filtered.groupby(['Product'])['Quantity Ordered'].sum().reset_index()
            fig_units_sold = px.bar(df_units_sold, x='Product', y='Quantity Ordered', title='Units Sold for {}'.format(selected_months_years[0]))
            graphs.append(dcc.Graph(id='units-sold-graph', figure=fig_units_sold))
        else:
            # Show a line chart when multiple months are selected
            df_units_sold = data_filtered.groupby(['Year', 'Month', 'Product'])['Quantity Ordered'].sum().reset_index()
            fig_units_sold = px.line(df_units_sold, x='Month', y='Quantity Ordered', color='Product', title='Units Sold per Month by Product')
            graphs.append(dcc.Graph(id='units-sold-graph', figure=fig_units_sold))
    
    # Show percentage of revenue by product 
    if 'percentage_sales' in selected_metrics:
        df_percentage_sales = data_filtered.groupby(['Year', 'Month', 'Product']).agg({'Revenue': 'sum', 'Quantity Ordered': 'sum'}).reset_index()
        df_percentage_sales['Percentage Revenue'] = df_percentage_sales.groupby(['Year', 'Month'])['Revenue'].apply(lambda x: x / x.sum() * 100)
        df_percentage_sales['Percentage Quantity'] = df_percentage_sales.groupby(['Year', 'Month'])['Quantity Ordered'].apply(lambda x: x / x.sum() * 100)
        fig_percentage_sales = px.bar(df_percentage_sales, x='Month', y='Percentage Revenue', color='Product', title='Percentage of Product Sales by Revenue')
        graphs.append(dcc.Graph(id='percentage-sales-graph', figure=fig_percentage_sales))

    return graphs

#Run the app

if __name__ == '__main__':
    app.run_server(debug=True)

