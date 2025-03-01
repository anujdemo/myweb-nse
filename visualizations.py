import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import numpy as np

def create_price_chart(stock_data, symbol, indicators):
    """Create main price chart with technical indicators"""
    # Create figure with secondary y-axis
    fig = make_subplots(rows=2, cols=1, 
                       shared_xaxes=True,
                       vertical_spacing=0.03,
                       row_heights=[0.7, 0.3])

    # Add candlestick
    fig.add_trace(
        go.Candlestick(
            x=stock_data.index,
            open=stock_data['Open'],
            high=stock_data['High'],
            low=stock_data['Low'],
            close=stock_data['Close'],
            name='Price',
            increasing_line_color='#26a69a',
            decreasing_line_color='#ef5350'
        ),
        row=1, col=1
    )

    # Add Moving Averages
    colors = {'MA20': '#1976D2', 'MA50': '#FFA000', 'MA200': '#E64A19'}
    for ma_name in ['MA20', 'MA50', 'MA200']:
        fig.add_trace(
            go.Scatter(
                x=stock_data.index,
                y=indicators[ma_name],
                name=ma_name,
                line=dict(color=colors[ma_name], width=1),
                opacity=0.7
            ),
            row=1, col=1
        )

    # Add Bollinger Bands
    for band, name in zip(['BB_Upper', 'BB_Middle', 'BB_Lower'], 
                         ['Upper BB', 'Middle BB', 'Lower BB']):
        fig.add_trace(
            go.Scatter(
                x=stock_data.index,
                y=indicators[band],
                name=name,
                line=dict(color='rgba(128, 128, 128, 0.3)', dash='dash'),
                opacity=0.5
            ),
            row=1, col=1
        )

    # Add RSI
    fig.add_trace(
        go.Scatter(
            x=stock_data.index,
            y=indicators['RSI'],
            name='RSI',
            line=dict(color='#9C27B0')
        ),
        row=2, col=1
    )

    # Add RSI reference lines
    for level in [30, 70]:
        fig.add_hline(
            y=level,
            line_dash="dash",
            line_color="gray",
            opacity=0.5,
            row=2
        )

    # Update layout
    fig.update_layout(
        title=f'{symbol} Technical Analysis',
        yaxis_title='Price (₹)',
        yaxis2_title='RSI',
        template='plotly_white',
        xaxis_rangeslider_visible=False,
        height=800,
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )

    # Update y-axes
    fig.update_yaxes(title_text="Price (₹)", row=1, col=1)
    fig.update_yaxes(title_text="RSI", row=2, col=1)

    return fig

def create_macd_chart(stock_data, indicators):
    """Create MACD chart"""
    fig = go.Figure()

    # Add MACD line
    fig.add_trace(
        go.Scatter(
            x=stock_data.index,
            y=indicators['MACD'],
            name='MACD',
            line=dict(color='#2962FF')
        )
    )

    # Add Signal line
    fig.add_trace(
        go.Scatter(
            x=stock_data.index,
            y=indicators['Signal'],
            name='Signal',
            line=dict(color='#FF6D00')
        )
    )

    # Add Histogram
    fig.add_trace(
        go.Bar(
            x=stock_data.index,
            y=indicators['Histogram'],
            name='Histogram',
            marker_color=np.where(indicators['Histogram'] >= 0, '#26a69a', '#ef5350')
        )
    )

    fig.update_layout(
        title='MACD Indicator',
        yaxis_title='Value',
        template='plotly_white',
        height=400,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    return fig

def create_returns_chart(stock_data, symbol):
    """Create returns chart with enhanced design"""
    returns = (stock_data['Close'] / stock_data['Close'].iloc[0] - 1) * 100

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=stock_data.index,
            y=returns,
            mode='lines',
            name='Returns',
            line=dict(color='#00BFA5', width=2),
            fill='tozeroy',
            fillcolor='rgba(0, 191, 165, 0.1)'
        )
    )

    fig.update_layout(
        title=f'{symbol} Cumulative Returns (%)',
        yaxis_title='Returns (%)',
        template='plotly_white',
        height=400,
        showlegend=False,
        hovermode='x unified'
    )

    return fig