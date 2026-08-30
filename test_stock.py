import yfinance as yf

stock = yf.Ticker("MRF.NS")
info = stock.info 
print(info["currentPrice"])
