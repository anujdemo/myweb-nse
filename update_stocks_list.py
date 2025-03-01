import pandas as pd
import trafilatura
import re

def get_nifty500_stocks():
    """Fetch Nifty 500 stocks list from NSE website"""
    try:
        # Since direct scraping might be restricted, using a predefined list
        # This is a comprehensive list of major Nifty stocks
        default_stocks = [
            # Nifty 50 stocks
            ("RELIANCE.NS", "Reliance Industries Ltd"),
            ("TCS.NS", "Tata Consultancy Services Ltd"),
            ("HDFCBANK.NS", "HDFC Bank Ltd"),
            ("INFY.NS", "Infosys Ltd"),
            ("ICICIBANK.NS", "ICICI Bank Ltd"),
            ("HINDUNILVR.NS", "Hindustan Unilever Ltd"),
            ("ITC.NS", "ITC Ltd"),
            ("SBIN.NS", "State Bank of India"),
            ("BHARTIARTL.NS", "Bharti Airtel Ltd"),
            ("KOTAKBANK.NS", "Kotak Mahindra Bank Ltd"),
            ("LICI.NS", "Life Insurance Corporation of India"),
            ("ADANIENT.NS", "Adani Enterprises Ltd"),
            ("HCLTECH.NS", "HCL Technologies Ltd"),
            ("ASIANPAINT.NS", "Asian Paints Ltd"),
            ("AXISBANK.NS", "Axis Bank Ltd"),
            ("MARUTI.NS", "Maruti Suzuki India Ltd"),
            ("WIPRO.NS", "Wipro Ltd"),
            ("SUNPHARMA.NS", "Sun Pharmaceutical Industries Ltd"),
            ("TATAMOTORS.NS", "Tata Motors Ltd"),
            ("ULTRACEMCO.NS", "UltraTech Cement Ltd"),
            ("TITAN.NS", "Titan Company Ltd"),
            ("BAJFINANCE.NS", "Bajaj Finance Ltd"),
            ("TATASTEEL.NS", "Tata Steel Ltd"),
            ("NESTLEIND.NS", "Nestle India Ltd"),
            ("LT.NS", "Larsen & Toubro Ltd"),
            ("POWERGRID.NS", "Power Grid Corporation of India Ltd"),
            ("M&M.NS", "Mahindra & Mahindra Ltd"),
            ("NTPC.NS", "NTPC Ltd"),
            ("TECHM.NS", "Tech Mahindra Ltd"),
            ("BAJAJFINSV.NS", "Bajaj Finserv Ltd"),
            ("ADANIGREEN.NS", "Adani Green Energy Ltd"),
            ("ADANIPORTS.NS", "Adani Ports and Special Economic Zone Ltd"),
            ("CIPLA.NS", "Cipla Ltd"),
            ("COALINDIA.NS", "Coal India Ltd"),
            ("GRASIM.NS", "Grasim Industries Ltd"),
            ("BAJAJ-AUTO.NS", "Bajaj Auto Ltd"),
            ("ONGC.NS", "Oil & Natural Gas Corporation Ltd"),
            ("DRREDDY.NS", "Dr. Reddy's Laboratories Ltd"),
            ("INDUSINDBK.NS", "IndusInd Bank Ltd"),
            ("BRITANNIA.NS", "Britannia Industries Ltd"),
            ("HINDALCO.NS", "Hindalco Industries Ltd"),
            ("DIVISLAB.NS", "Divi's Laboratories Ltd"),
            ("APOLLOHOSP.NS", "Apollo Hospitals Enterprise Ltd"),
            ("JSWSTEEL.NS", "JSW Steel Ltd"),
            ("ADANIENT.NS", "Adani Enterprises Ltd"),
            ("TATAMOTORS.NS", "Tata Motors Ltd"),
            ("SBILIFE.NS", "SBI Life Insurance Company Ltd"),
            ("HDFCLIFE.NS", "HDFC Life Insurance Company Ltd"),
            ("UPL.NS", "UPL Ltd"),
            ("EICHERMOT.NS", "Eicher Motors Ltd"),

            # Additional Large Cap Stocks
            ("PIDILITIND.NS", "Pidilite Industries Ltd"),
            ("GODREJCP.NS", "Godrej Consumer Products Ltd"),
            ("SIEMENS.NS", "Siemens Ltd"),
            ("DABUR.NS", "Dabur India Ltd"),
            ("HAVELLS.NS", "Havells India Ltd"),
            ("DLF.NS", "DLF Ltd"),
            ("INDIGO.NS", "InterGlobe Aviation Ltd"),
            ("JUBLFOOD.NS", "Jubilant FoodWorks Ltd"),
            ("VEDL.NS", "Vedanta Ltd"),
            ("MCDOWELL-N.NS", "United Spirits Ltd"),
            ("HEROMOTOCO.NS", "Hero MotoCorp Ltd"),
            ("BOSCHLTD.NS", "Bosch Ltd"),
            ("GODREJPROP.NS", "Godrej Properties Ltd"),
            ("LUPIN.NS", "Lupin Ltd"),
            ("ZOMATO.NS", "Zomato Ltd"),
            ("NYKAA.NS", "FSN E-Commerce Ventures Ltd"),
            ("DMART.NS", "Avenue Supermarts Ltd"),

            # Banking and Financial Sector
            ("PNB.NS", "Punjab National Bank"),
            ("BANDHANBNK.NS", "Bandhan Bank Ltd"),
            ("UNIONBANK.NS", "Union Bank of India"),
            ("CANBK.NS", "Canara Bank"),
            ("BANKBARODA.NS", "Bank of Baroda"),
            ("FEDERALBNK.NS", "The Federal Bank Ltd"),
            ("IDFCFIRSTB.NS", "IDFC First Bank Ltd"),
            ("AUBANK.NS", "AU Small Finance Bank Ltd"),

            # Energy and Power Sector
            ("IOC.NS", "Indian Oil Corporation Ltd"),
            ("GAIL.NS", "GAIL (India) Ltd"),
            ("TATAPOWER.NS", "Tata Power Co. Ltd"),
            ("NHPC.NS", "NHPC Ltd"),
            ("RECLTD.NS", "REC Ltd"),
            ("PFC.NS", "Power Finance Corporation Ltd"),
            ("TORNTPOWER.NS", "Torrent Power Ltd"),
            ("ADANIPOWER.NS", "Adani Power Ltd"),

            # IT and Technology
            ("MINDTREE.NS", "MindTree Ltd"),
            ("LTTS.NS", "L&T Technology Services Ltd"),
            ("PERSISTENT.NS", "Persistent Systems Ltd"),
            ("MPHASIS.NS", "Mphasis Ltd"),
            ("COFORGE.NS", "Coforge Ltd"),

            # Pharma and Healthcare
            ("BIOCON.NS", "Biocon Ltd"),
            ("ALKEM.NS", "Alkem Laboratories Ltd"),
            ("TORNTPHARM.NS", "Torrent Pharmaceuticals Ltd"),
            ("AUROPHARMA.NS", "Aurobindo Pharma Ltd"),
            ("FORTIS.NS", "Fortis Healthcare Ltd"),

            # Automobile and Auto Components
            ("ASHOKLEY.NS", "Ashok Leyland Ltd"),
            ("BALKRISIND.NS", "Balkrishna Industries Ltd"),
            ("MRF.NS", "MRF Ltd"),
            ("MOTHERSON.NS", "Motherson Sumi Systems Ltd"),
            ("TVSMOTOR.NS", "TVS Motor Company Ltd"),

            # Consumer Goods
            ("COLPAL.NS", "Colgate-Palmolive (India) Ltd"),
            ("MARICO.NS", "Marico Ltd"),
            ("TATACONSUM.NS", "Tata Consumer Products Ltd"),
            ("VBL.NS", "Varun Beverages Ltd"),
            ("EMAMILTD.NS", "Emami Ltd")
        ]

        # Create DataFrame and save to CSV
        df = pd.DataFrame(default_stocks, columns=['Symbol', 'Name'])
        df.to_csv('nifty500_symbols.csv', index=False)
        return True
    except Exception as e:
        print(f"Error updating stock list: {str(e)}")
        return False

if __name__ == "__main__":
    get_nifty500_stocks()