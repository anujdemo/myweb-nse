import streamlit as st
import pandas as pd
from data_handler import StockDataHandler
from visualizations import create_price_chart, create_macd_chart, create_returns_chart
from technical_analysis import calculate_all_indicators
from utils import format_percentage, format_price
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Indian Stock Market Analysis",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 0rem 1rem;
    }
    .stApp {
        background-color: #f8f9fa;
    }
    .css-1d391kg {
        padding-top: 1rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'data_handler' not in st.session_state:
    st.session_state.data_handler = StockDataHandler()

# Sidebar
with st.sidebar:
    st.title("📊 Controls")

    # Auto-refresh settings
    st.subheader("Data Updates")
    auto_refresh = st.checkbox('Enable Auto-refresh', value=True)
    if auto_refresh:
        time.sleep(60)
        st.rerun()

    # Time period selection
    st.subheader("Time Range")
    period_options = {
        '1 Month': '1mo',
        '3 Months': '3mo',
        '6 Months': '6mo',
        '1 Year': '1y',
        '2 Years': '2y',
        '5 Years': '5y'
    }
    selected_period = st.select_slider(
        "Select Time Period",
        options=list(period_options.keys())
    )

    # Price filters
    st.subheader("Price Filters")
    filter_options = [
        "All Stocks",
        "Near 52-Week High",
        "Near 52-Week Low"
    ]
    price_filter = st.radio(
        "Select Filter",
        filter_options
    )

# Main content
st.title("📈 Indian Stock Market Analysis")
st.markdown("""
This advanced tool provides real-time analysis for Nifty 500 stocks with technical indicators
and comprehensive price analytics.
""")

# Load and filter data
with st.spinner("Loading stock data..."):
    try:
        stocks_df = st.session_state.data_handler.get_stock_data(
            period_options[selected_period]
        )

        if price_filter == "Near 52-Week High":
            stocks_df = st.session_state.data_handler.filter_near_52week_high(stocks_df)
        elif price_filter == "Near 52-Week Low":
            stocks_df = st.session_state.data_handler.filter_near_52week_low(stocks_df)

        # Market Overview Section
        st.header("Market Overview")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Total Stocks",
                len(stocks_df),
                delta=None
            )
        with col2:
            avg_1y_return = stocks_df['1y_return'].mean()
            st.metric(
                "Average 1Y Return",
                format_percentage(avg_1y_return),
                delta=format_percentage(avg_1y_return)
            )
        with col3:
            avg_5y_return = stocks_df['5y_return'].mean()
            st.metric(
                "Average 5Y Return",
                format_percentage(avg_5y_return),
                delta=format_percentage(avg_5y_return)
            )
        with col4:
            last_update = st.session_state.data_handler.get_last_update_time()
            if last_update:
                st.metric(
                    "Last Updated",
                    last_update.strftime("%H:%M:%S"),
                    delta="Live" if auto_refresh else None
                )

        # Stock Analysis Section
        st.header("Stock Analysis")

        # Search and filter
        search = st.text_input("🔍 Search stocks by name or symbol")
        if search:
            stocks_df = stocks_df[
                stocks_df['Symbol'].str.contains(search, case=False) |
                stocks_df['Name'].str.contains(search, case=False)
            ]

        # Display stock table with enhanced styling
        st.dataframe(
            stocks_df[[
                'Symbol', 'Name', 'Current Price', 'Price Change %',
                '52W High', '52W Low', 'From 52W High %', 'From 52W Low %',
                '1y_return', '2y_return', '5y_return'
            ]].style.format({
                'Current Price': '₹{:.2f}',
                'Price Change %': '{:+.2f}%',
                '52W High': '₹{:.2f}',
                '52W Low': '₹{:.2f}',
                'From 52W High %': '{:.1f}%',
                'From 52W Low %': '{:+.1f}%',
                '1y_return': '{:.2%}',
                '2y_return': '{:.2%}',
                '5y_return': '{:.2%}'
            }).applymap(
                lambda x: 'color: red' if isinstance(x, float) and x < 0 else 'color: green',
                subset=['Price Change %', 'From 52W High %', 'From 52W Low %', '1y_return', '2y_return', '5y_return']
            ).set_properties(**{
                'background-color': 'white',
                'font-family': 'sans-serif'
            }),
            height=400
        )

        # Technical Analysis Section
        st.header("Technical Analysis")

        selected_stock = st.selectbox(
            "Select a stock for detailed analysis",
            stocks_df['Symbol'].tolist()
        )

        if selected_stock:
            stock_data = st.session_state.data_handler.get_detailed_stock_data(
                selected_stock,
                period_options[selected_period]
            )

            # Calculate technical indicators
            indicators = calculate_all_indicators(stock_data)

            # Create tabs for different charts
            tab1, tab2, tab3 = st.tabs(["📊 Price & Indicators", "📉 MACD", "📈 Returns"])

            with tab1:
                st.plotly_chart(
                    create_price_chart(stock_data, selected_stock, indicators),
                    use_container_width=True
                )

            with tab2:
                st.plotly_chart(
                    create_macd_chart(stock_data, indicators),
                    use_container_width=True
                )

            with tab3:
                st.plotly_chart(
                    create_returns_chart(stock_data, selected_stock),
                    use_container_width=True
                )

            # Technical Indicators Summary
            st.subheader("Technical Indicators Summary")
            col1, col2, col3 = st.columns(3)

            with col1:
                current_rsi = indicators['RSI'].iloc[-1]
                rsi_status = "Oversold" if current_rsi < 30 else "Overbought" if current_rsi > 70 else "Neutral"
                st.metric("RSI (14)", f"{current_rsi:.2f}", rsi_status)

            with col2:
                macd = indicators['MACD'].iloc[-1]
                signal = indicators['Signal'].iloc[-1]
                macd_status = "Bullish" if macd > signal else "Bearish"
                st.metric("MACD", f"{macd:.2f}", macd_status)

            with col3:
                current_price = stock_data['Close'].iloc[-1]
                ma200 = indicators['MA200'].iloc[-1]
                trend = "Above MA200" if current_price > ma200 else "Below MA200"
                st.metric("Trend", trend, f"{((current_price/ma200 - 1) * 100):.2f}%")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Add refresh button
if st.button("🔄 Refresh Data"):
    st.session_state.data_handler.clear_cache()
    st.experimental_rerun()

# Footer
st.markdown("""
---
<div style='text-align: center'>
    <p>Real-time data provided by Yahoo Finance. Auto-refreshes every minute when enabled.</p>
    <p>Last updated: {}</p>
</div>
""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)