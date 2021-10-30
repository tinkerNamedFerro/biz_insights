import dash
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px

def showSingleLineGraphMarket(df):
    
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
            ]),
        
        html.Div(id='output-container-range-slider'),
        dcc.Graph(id="line-chart"),
    ])

    @app.callback(
        dash.dependencies.Output("line-chart", "figure"),
        [dash.dependencies.Input('my-range-slider', 'value')])
    def update_line_chart(value):
        # converting 1-10 to market cap intervals
        transformed_value = [transform_value(v) for v in value]
        print(transformed_value)
        # Make mask where true if in range
        mask = (df.marketCap >= transformed_value[0]) & (df.marketCap <= transformed_value[1])
        # Only show rows where mask is true
        fig = px.line(df[mask], x="Time", y="Mentions", color='ticker', height=800)
        return fig
        #return 'You have selected "{}"'.format(value)

    app.run_server(debug=True)