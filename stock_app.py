import datetime
import streamlit as st
import yfinance as yf # https://pypi.org/project/yfinance/
from ta.volatility import BollingerBands
from ta.trend import MACD
from ta.momentum import RSIIndicator

from PIL import Image

##################
# Set up sidebar #
##################

# Add in location to select image.
st.sidebar.markdown("<h1 style='text-align: center; color: #d84519;'>Stock Analyst</h1>", unsafe_allow_html=True)

ticker = st.sidebar.text_input('Add ticker') #, ( 'AAPL', 'MSFT',"SPY",'WMT'))

today = datetime.date.today()
before = today - datetime.timedelta(days=1000)
start_date = st.sidebar.date_input('Start date', before)
end_date = st.sidebar.date_input('End date', today)
# if start_date < end_date:
#     st.sidebar.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
# else:
#     st.sidebar.error('Error: End date must fall after start date.')

image = Image.open('www/afi_logo.png')
st.sidebar.image(image)

##############
# Stock data #
##############

# https://technical-analysis-library-in-python.readthedocs.io/en/latest/ta.html#momentum-indicators
if ticker:
	
	# Get ticker info
	ticker_info = yf.Ticker(ticker)
	
	# Ticker info
	st.markdown(f"<h1 style='text-align: center; color: #d84519;'>{ticker_info.info['longName']}</h1>", unsafe_allow_html=True)
	col1, col2 = st.beta_columns([1, 3])
	
	col1.image(ticker_info.info['logo_url'])
	col1.markdown(f"**Sector:** {ticker_info.info['sector']}")
	col1.markdown(f"**Country:** {ticker_info.info['country']}")
	
	ticker_summary = ticker_info.info['longBusinessSummary'][:500] + '...'
	col2.markdown(f"{ticker_summary}")
	
	# Get data
	df = yf.download(ticker,start= start_date,end= end_date, progress=False)
	
	# Bollinger Bands
	st.markdown(f"<h3 style='text-align: center; color: #d84519;'>Bollinger Bands</h3>", unsafe_allow_html=True)
	indicator_bb = BollingerBands(df['Close'])
	
	bb = df
	bb['bb_h'] = indicator_bb.bollinger_hband()
	bb['bb_l'] = indicator_bb.bollinger_lband()
	bb = bb[['Close','bb_h','bb_l']]
	
	st.line_chart(bb)
	
	# MACD
	st.markdown(f"<h3 style='text-align: center; color: #d84519;'>MACD (Moving Average Convergence Divergence)</h3>", unsafe_allow_html=True)
	macd = MACD(df['Close']).macd()
	
	st.area_chart(macd)
	
	# RSI
	st.markdown(f"<h3 style='text-align: center; color: #d84519;'>RSI</h3>", unsafe_allow_html=True)
	rsi = RSIIndicator(df['Close']).rsi()
	
	st.line_chart(rsi)
	
	# Recent data
	st.write('Recent data ')
	st.dataframe(df.tail(10))



