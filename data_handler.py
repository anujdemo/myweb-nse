import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st

class StockDataHandler:
    def __init__(self):
        self.nifty500_symbols = self._load_nifty500_symbols()
        self.last_update_time = None

    @st.cache_data(ttl=3600)
    def _load_nifty500_symbols(_self):  # Changed 'self' to '_self' for caching
        # Load Nifty 500 symbols from CSV
        try:
            df = pd.read_csv('nifty500_symbols.csv')
            st.write(f"Loaded {len(df)} stocks from CSV")  # Debug info
            return df
        except Exception as e:
            st.error(f"Error loading CSV: {str(e)}")
            # Fallback to a smaller list if file not found
            return pd.DataFrame({
                'Symbol': ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS'],
                'Name': ['Reliance Industries', 'Tata Consultancy Services', 'HDFC Bank']
            })

    def get_real_time_price(self, symbol):
        """Get real-time price for a single symbol"""
        try:
            ticker = yf.Ticker(symbol)
            live_data = ticker.history(period='1d', interval='1m')
            if len(live_data) > 0:
                return live_data['Close'].iloc[-1]
            return None
        except Exception as e:
            st.warning(f"Error fetching price for {symbol}: {str(e)}")
            return None

    @st.cache_data(ttl=60)  # Cache for 1 minute
    def get_stock_data(_self, period='1y', include_live_prices=True):
        try:
            st.info("Fetching stock data...")  # Debug info
            stocks_data = []

            for _, row in _self.nifty500_symbols.iterrows():
                try:
                    ticker = yf.Ticker(row['Symbol'])
                    hist = ticker.history(period='5y')

                    if len(hist) == 0:
                        continue

                    # Get historical data
                    historical_price = hist['Close'][-1]
                    high_52w = hist['High'][-252:].max() if len(hist) >= 252 else historical_price
                    low_52w = hist['Low'][-252:].min() if len(hist) >= 252 else historical_price

                    # Get real-time price if requested
                    current_price = _self.get_real_time_price(row['Symbol']) if include_live_prices else historical_price
                    if current_price is None:
                        current_price = historical_price

                    # Calculate price change and 52-week metrics
                    price_change = ((current_price - historical_price) / historical_price) * 100
                    pct_from_high = ((high_52w - current_price) / high_52w) * 100  # How far below 52w high
                    pct_from_low = ((current_price - low_52w) / low_52w) * 100  # How far above 52w low

                    returns = {
                        '1y_return': (hist['Close'][-1] / hist['Close'][-252] - 1) if len(hist) >= 252 else np.nan,
                        '2y_return': (hist['Close'][-1] / hist['Close'][-504] - 1) if len(hist) >= 504 else np.nan,
                        '5y_return': (hist['Close'][-1] / hist['Close'][0] - 1) if len(hist) >= 1260 else np.nan
                    }

                    stocks_data.append({
                        'Symbol': row['Symbol'],
                        'Name': row['Name'],
                        'Current Price': current_price,
                        'Price Change %': price_change,
                        '52W High': high_52w,
                        '52W Low': low_52w,
                        'From 52W High %': pct_from_high,
                        'From 52W Low %': pct_from_low,
                        **returns
                    })

                except Exception as e:
                    st.warning(f"Error processing {row['Symbol']}: {str(e)}")
                    continue

            _self.last_update_time = datetime.now()
            df = pd.DataFrame(stocks_data)
            st.write(f"Processed {len(df)} stocks successfully")  # Debug info
            return df

        except Exception as e:
            st.error(f"Error in get_stock_data: {str(e)}")
            return pd.DataFrame()  # Return empty DataFrame on error

    def filter_near_52week_high(self, df, threshold=0.95):
        return df[df['Current Price'] >= df['52W High'] * threshold]

    def filter_near_52week_low(self, df, threshold=1.05):
        return df[df['Current Price'] <= df['52W Low'] * threshold]

    @st.cache_data(ttl=60)  # Cache for 1 minute
    def get_detailed_stock_data(_self, symbol, period='1y'):
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            return hist
        except Exception as e:
            st.error(f"Error getting detailed data for {symbol}: {str(e)}")
            return pd.DataFrame()

    def clear_cache(self):
        st.cache_data.clear()

    def get_last_update_time(self):
        return self.last_update_time