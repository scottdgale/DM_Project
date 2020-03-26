import pandas as pd

print("Exploring Data.")

stocks = pd.read_csv("2016.csv")
ticker_symbols = stocks.iloc[:,0]
