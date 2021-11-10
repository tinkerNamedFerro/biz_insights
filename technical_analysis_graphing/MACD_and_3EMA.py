import pandas_ta as ta
from datetime import datetime
import plotly.graph_objects as go


def get3EMA(group, fig):
    group["EMA9"] = group.ta.ema(close=group.Mentions, length=9, suffix="EMA9")
    group["EMA21"] = group.ta.ema(close=group.Mentions, length=21, suffix="EMA21")
    group["EMA50"] = group.ta.ema(close=group.Mentions, length=50, suffix="EMA50")
    fig.add_trace(go.Scatter(x=group.Time, y=group.EMA9,
                mode='lines',
                name='EMA9'), 
            row=1,
            col=1,
            secondary_y=False)
    fig.add_trace(go.Scatter(x=group.Time, y=group.EMA21,
                mode='lines',
                name='EMA21'), 
            row=1,
            col=1,
            secondary_y=False)
    fig.add_trace(go.Scatter(x=group.Time, y=group.EMA50,
                mode='lines',
                name='EMA50'), 
            row=1,
            col=1,
            secondary_y=False)
    return group, fig

#fig = make_subplots(rows=2, cols=1, specs=[[{"secondary_y": True}],[{}]])   
def getMACD(group, fig):
    group.ta.macd(close='Mentions', fast=12, slow=26, signal=9, append=True)
    group.dropna(subset = ["MACD_12_26_9", "MACDh_12_26_9", "MACDs_12_26_9"], inplace=True)
    print(group)
                # Fast Signal (%k)
    fig.append_trace(
        go.Scatter(
            x=group.Time,
            y=group['MACD_12_26_9'],
            line=dict(color='#ff9900', width=2),
            name='macd',
            # showlegend=False,
            legendgroup='2',
        ), row=2, col=1
    )
    # Slow signal (%d)
    fig.append_trace(
        go.Scatter(
            x=group.Time,
            y=group['MACDs_12_26_9'],
            line=dict(color='#000000', width=2),
            # showlegend=False,
            legendgroup='2',
            name='signal'
        ), row=2, col=1
    )
    # Colorize the histogram values
    colors = np.where(group['MACDh_12_26_9'] < 0, '#000', '#ff9900')
    # Plot the histogram
    fig.append_trace(
        go.Bar(
            x=group.Time,
            y=group['MACDh_12_26_9'],
            name='histogram',
            marker_color=colors,
        ), row=2, col=1
    )   
    return fig