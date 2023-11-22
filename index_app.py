# STOCKS-ANALYSER
# IMPORTING RELEVANT LIBRARIES
import dash
from dash import dcc
from dash import html
from datetime import datetime as date
import dash_bootstrap_components as dbc
import pandas as pd
import requests
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import plotly.express as px
from dash.exceptions import PreventUpdate
from pandas_datareader import data as pdr
# Model
from model import prediction
from sklearn.svm import SVR

external_stylesheets = [
    'https://fonts.googleapis.com/css2?family=El+Messiri&family=Shantell+Sans:ital,wght@1,600&display=swap']

# Creating Dash Instance and Storing Application Server Properties
app = dash.Dash(__name__, title="TradeAIalytics",
                external_stylesheets=external_stylesheets)
app.css.config.serve_locally = True
server = app.server


# Your Financial Modeling Prep API key
api_key = '857f4ca5ee54bfc92d5079a735622259'
# Define the base URL for the Financial Modeling Prep API
base_url = 'https://financialmodelingprep.com/api/v3/'

# Layout
navbar = html.Div([
    html.Div([
        html.H1('TradeAIalytics', className='web-name'),
        html.Div([
            html.Div(className='circle', id='circle1'),
            html.Div(className='circle', id='circle2'),
            html.Div(className='circle', id='circle3'),
        ], className='circle_design')
    ], className='nav-content'),
], id='navbar')

body = html.Div([
    html.Div([
        html.Div([
            html.Div([
                # stock code input
                html.Label('Please Enter Stock Code: ',
                           className='stock-input-label'),
                dcc.Input(id='input-box',
                          value='', type='text', placeholder='Enter a Stock code'),
                html.Button('Submit', id='submit-button', n_clicks=0),
            ], className='stock-input-div'),
            html.Div([
                # Date Range Picker input
                'Please Select a Date Range:  ',
                dcc.DatePickerRange(
                    id='date-picker-range',
                    min_date_allowed=date(1995, 8, 5),
                    display_format="YY-MM-DD",
                    max_date_allowed=date.now(),
                    initial_visible_month=date.now(),
                    end_date=date.now().date(),
                    className='custom-date-picker'
                ),
                html.Div(id='output-container-date-picker-range')

            ], className='date-picker-div'),
            html.Div([
                html.Div([
                    # Stock price button
                    html.Button('Stock Price',
                                id='stock-price-button', n_clicks=0),
                    # Indicators button
                    html.Button(
                        'Indicators', id='indicator-button', n_clicks=0)
                ], className='stock-price-indicator-div'),
                # Number of days of forecast input
                html.Div([
                    html.Label('Please Enter a Number of Days:  ',
                               className='days-input-label'),
                    dcc.Input(id='input-forecast-days',
                              placeholder='Enter no. of Days', type='number'),
                    # Forecast button
                    html.Button('Forecast', id='forecast-button', n_clicks=0)
                ], className='forecast-div'),
            ]),
        ], className='input-div')
    ], className='div-input-section'),
    # Div-2 (for Data Plots and company Information)
    html.Div([
        html.Div([
            # Company Name
            html.Img(id="logo"),
            html.H1(id='name')
        ], className='header'),
        html.Div(
            # Description
            id='description', className='decription_ticker'),
        html.Div([
            # Stock price plot
        ], id='graphs-content'),
        html.Div([
            # Indicator plot
        ], id='main-content'),
        html.Div([
            # Forecast plot
        ], id='forecast-content')
    ],
        className='content')
], className='container')
app.layout = html.Div(children=[
    navbar,
    body
])

# all callbacks for Stocks-code input


@app.callback([
    Output('description', 'children'),
    Output("logo", "src"),
    Output('name', 'children'),
    Output('stock-price-button', 'n_clicks'),
    Output('indicator-button', 'n_clicks'),
    Output('forecast-button', 'n_clicks'),
    Input('submit-button', 'n_clicks'),
    State('input-box', 'value')
])
# this functions updates values as per above callbacks
def update_data(n, val):
    if n == None:
        return "Hey there! Please enter a legitimate stock code to get details."
    if val == None:
        # raise preventupdate
        raise PreventUpdate
    else:
        endpoint = f'profile/{val}?apikey={api_key}'
        url = base_url + endpoint
        # Send the API request
        response = requests.get(url)
        # Check the response status
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            df[['companyName', 'description', 'image']]
            return df['description'].values[0], df['image'].values[0], df['companyName'].values[0], None, None, None

# # all callbacks for date-range-pickers stock-price button


@app.callback([
    Output('graphs-content', 'children'),
    Input('stock-price-button', 'n_clicks'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'),
    State('input-box', 'value')
])
# this functions updates values as per above callbacks
def update_graph(n, start_date, end_date, val):
    if n == None:
        return [""]
    # raise PreventUpdate
    if val == None:
        raise PreventUpdate
    else:
        if start_date != None:
            endpoint = f'historical-chart/1day/{val}?from={start_date}&to={end_date}&apikey={api_key}'
            url = base_url + endpoint
            response = requests.get(url)
            data = response.json()
            df = pd.DataFrame(data)
            fig = px.line(df, x="date", y=[
                          "close", "open"], title="Closing and Opening Price vs Date", markers=True)
            return [dcc.Graph(figure=fig)]
        else:
            endpoint = f'historical-price-full/{val}?apikey={api_key}'
            url = base_url + endpoint
            response = requests.get(url)
            data = response.json()
            df = pd.DataFrame(data['historical'])
            fig = px.line(df, x="date", y=[
                          "close", "open"], title="Closing and Opening Price vs Date", markers=True)
            return [dcc.Graph(figure=fig)]

# all callbacks for date picker indicator buttons


@app.callback([
    Output("main-content", "children"),
    Input("indicator-button", "n_clicks"),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'),
    State("input-box", "value")
])
# this functions updates values as per above callbacks
def indicators(n, start_date, end_date, val):
    if n == None:
        return [""]
    if val == None:
        return [""]
    if start_date == None:
        endpoint = f'historical-price-full/{val}?apikey={api_key}'
        url = base_url + endpoint
        response = requests.get(url)
        data = response.json()
        df = pd.DataFrame(data['historical'])
        df['EWA_20'] = df['close'].ewm(span=20, adjust=False).mean()
        fig = px.scatter(df, x="date", y="EWA_20",
                         title="Exponential Moving Average vs Date")
        fig.update_traces(mode="lines+markers")
        return [dcc.Graph(figure=fig)]
    else:
        endpoint = f'historical-chart/1day/{val}?from={start_date}&to={end_date}&apikey={api_key}'
        url = base_url + endpoint
        response = requests.get(url)
        data = response.json()
        df = pd.DataFrame(data)
        df.reset_index(inplace=True)
        df['EWA_20'] = df['close'].ewm(span=20, adjust=False).mean()
        fig = px.scatter(df, x="date", y="EWA_20",
                         title="Exponential Moving Average vs Date")
        fig.update_traces(mode="lines+markers")
        return [dcc.Graph(figure=fig)]

# now this callback for forecasting


@app.callback([
    Output("forecast-content", "children"),
    Input("forecast-button", "n_clicks"),
    State("input-forecast-days", "value"),
    State("input-box", "value")
])
# function for above callback
def forecast(n, n_days, val):
    if n == None:
        return [""]
    if val == None:
        raise PreventUpdate
    endpoint = f'historical-price-full/{val}?apikey={api_key}'
    url = base_url + endpoint
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data['historical'])
    data_set = df.head(50)
    fig = prediction(val, int(n_days) + 1, data_set)
    return [dcc.Graph(figure=fig)]


# run on server
if __name__ == '__main__':
    app.run_server(debug=True)
