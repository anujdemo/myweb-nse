def format_percentage(value):
    """Format a decimal value as a percentage string"""
    try:
        return f"{value:.2%}"
    except:
        return "N/A"

def format_price(value):
    """Format a number as a price string with Indian Rupee symbol"""
    try:
        return f"₹{value:,.2f}"
    except:
        return "N/A"
