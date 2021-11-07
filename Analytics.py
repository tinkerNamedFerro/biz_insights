from re import template
import dash
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px

import plotly.graph_objects as go
from plotly.subplots import make_subplots
# import dash_daq as daq

from data_parsing import *

def showSingleLineGraphMarket():
    df = getAllTickerData()

    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    
    # Use the following function when accessing the value of 'my-range-slider'
    # in callbacks to transform the output value to logarithmic
    def transform_value(value):
        switcher={
                0:0,
                1:10000000, #10M
                2:50000000, #50M
                3:100000000,  #100M
                4:500000000,  #500M
                5:1000000000,   #1B
                6:10000000000,  #10B
                7:50000000000,  #50B
                8:100000000000, #100B
                9:500000000000, #500B
                10:1000000000000, #1T
                11:2000000000000 #2T
             }
        return switcher.get(value,"Invalid day of week")

    # Drop of all tickers and an addition option to show all
    dropDownOptions =  [{'label': "ALL", 'value': "ALL"}]
    for i in df.ticker.unique():
        dropDownOptions.append({'label': i, 'value': i})

    app.layout = html.Div([
         dbc.Form(
            [
                dbc.Label(
                    "Market Cap",
                    html_for="stroke-width",
                ),
                # Slider for specifying stroke width
                dcc.RangeSlider(
                    id='my-range-slider',
                    min=0,
                    max=11,
                    step=None,
                    allowCross=False,
                    marks={
                        0: '0',
                        1: '10M',
                        2: '50M',
                        3: '100M',
                        4: '500M',
                        5: '1B',
                        6: '10B',
                        7: '50B',
                        8: '100B',
                        9: '500B',
                        10: '1T',
                        11: '2T',
                    },
                    value=[0, 11]
                ),
                # dbc.Label(
                #     "Minimum Average Daily Mentions",
                #     html_for="stroke-width",
                # ),
                # html.I("Try typing in input 1 & 2, and observe how debounce is impacting the callbacks. Press Enter and/or Tab key in Input 2 to cancel the delay"),
                # html.Br(),
                # dcc.Input(id="input1", type="text", placeholder="", style={'marginRight':'10px'}),
                # dcc.Input(id="input2", type="text", placeholder="", debounce=True),
                # html.Div(id="output"),
                dcc.Dropdown(
                    id='demo-dropdown',
                    options=dropDownOptions,
                    value='ALL'
                ),
            ]),
        
        html.Div(id='output-container-range-slider'),
        dcc.Graph(id="line-chart"),
    ])
    #  Market Cap and ticker selector 
    @app.callback(
        dash.dependencies.Output("line-chart", "figure"),
        [dash.dependencies.Input('my-range-slider', 'value'),dash.dependencies.Input('demo-dropdown', 'value')])
    def update_line_chart(market, ticker_selector):
        # converting 1-10 to market cap intervals
        transformed_value = [transform_value(v) for v in market]
        # Make mask where true if in range
        marketCapMask = (df.marketCap >= transformed_value[0]) & (df.marketCap <= transformed_value[1])

        # ticker selector
        if ticker_selector and ticker_selector != "ALL": 
            tickerMask  = (df.ticker.str.contains(ticker_selector)) == False
        else:
            tickerMask  = (df.ticker.str.contains("ALL")) == True
       
        # Create figure with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        # Only show rows where mask is true
    

        graphingDf = df[~(marketCapMask & tickerMask)]
        grouped = graphingDf.groupby('ticker')

        for name, group in grouped:
            fig.add_trace(go.Scatter(x=group.Time, y=group.Mentions,# color='ticker',
                        mode='lines',
                        name=name),
                    secondary_y=False)
        # Show price when only one coin is selected
        if ticker_selector and ticker_selector != "ALL": 
            priceDF = getChartById( graphingDf['coinGeckoId'].iloc[0])
            fig.add_trace(go.Scatter(x=priceDF.Time, y=priceDF.Price,
                        mode='lines',
                        name='Price'),
                    secondary_y=True)

        fig.update_layout(
            autosize=False,
            # width=500,
            height=800,
            # margin=dict(
            #     l=50,
            #     r=50,
            #     b=100,
            #     t=100,
            #     pad=4
            # ),
            template="plotly_dark"
        )

        return fig

    app.run_server(debug=True)
    


showSingleLineGraphMarket()