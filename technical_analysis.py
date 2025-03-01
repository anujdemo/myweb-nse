import pandas as pd
import numpy as np

def calculate_rsi(data, periods=14):
    """Calculate Relative Strength Index"""
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(data, fast=12, slow=26, signal=9):
    """Calculate MACD (Moving Average Convergence Divergence)"""
    exp1 = data['Close'].ewm(span=fast, adjust=False).mean()
    exp2 = data['Close'].ewm(span=slow, adjust=False).mean()
    macd = exp1 - exp2
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    histogram = macd - signal_line
    return macd, signal_line, histogram

def calculate_moving_averages(data):
    """Calculate Multiple Moving Averages"""
    ma20 = data['Close'].rolling(window=20).mean()
    ma50 = data['Close'].rolling(window=50).mean()
    ma200 = data['Close'].rolling(window=200).mean()
    return ma20, ma50, ma200

def calculate_bollinger_bands(data, window=20):
    """Calculate Bollinger Bands"""
    ma = data['Close'].rolling(window=window).mean()
    std = data['Close'].rolling(window=window).std()
    upper_band = ma + (std * 2)
    lower_band = ma - (std * 2)
    return upper_band, ma, lower_band

def calculate_all_indicators(data):
    """Calculate all technical indicators"""
    indicators = {}
    
    # RSI
    indicators['RSI'] = calculate_rsi(data)
    
    # MACD
    indicators['MACD'], indicators['Signal'], indicators['Histogram'] = calculate_macd(data)
    
    # Moving Averages
    indicators['MA20'], indicators['MA50'], indicators['MA200'] = calculate_moving_averages(data)
    
    # Bollinger Bands
    indicators['BB_Upper'], indicators['BB_Middle'], indicators['BB_Lower'] = calculate_bollinger_bands(data)
    
    return indicators
