import plotly.express as px
import pandas as pd

# df stands for data frame.
# df = pd.read_json('../data.json')
# print(df)
# df = px.data.gapminder().query("continent=='Oceania'")
# print(df)
# fig = px.line(df, x="year", y="lifeExp", color='country')
# fig.show()

def showSingleLineGraph(df):
    fig = px.line(df, x="Time", y="Mentions", color='ticker')
    fig.show()