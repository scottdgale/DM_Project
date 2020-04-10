import yfinance as yf
import pandas as pd

print("Data Mining - Yahoo Finance API.")
stocks = pd.read_csv("data\stock_s.csv")
sectors = pd.read_csv("data\sectors.csv")

# 30 days prior to the election to 30 days after the election (60 days of data)
years = [['2016-9-28', '2016-12-22'], ['2012-9-24', '2012-12-20'], ['2008-9-24', '2008-12-18'],
        ['2004-9-22', '2004-12-16'], ['2000-9-27', '2000-12-21'], ['1996-9-25', '1996-12-19'],
        ['1992-9-23', '1992-12-17'], ['1988-9-28', '1988-12-22'], ['1984-9-26', '1984-12-20'],
        ['1980-9-22', '1980-12-17']]

year_string = ['2016', '2012', '2008', '2004', '2000', '1996', '1992', '1988', '1984', '1980']
election_code = ['DR', 'DD', 'RD', 'RR', 'DR', 'DD', 'RD', 'RR', 'RR', 'DR']
election_date = []

# 11/4/1980
# 11/6/1984
# 11/8/1988
# 11/3/1992
# 11/5/1996
# 11/7/2000
# 11/2/2004
# 11/4/2008
# 11/6/2012
# 11/8/2016

# UPDATE PATH FOR FILE
# path = 'data\election_data_close_norm.csv'
path = r'data\test.csv'

# used for testing
# tickerSymbol = 'GM'
# #get data on this ticker
# tickerData = yf.Ticker(tickerSymbol)
# #get the historical prices for this ticker
# tickerDf = tickerData.history(period='1d', start=years[2][0], end=years[2][1])

# Loop for #stocks in a given year
yearly_data = []
for i in range(stocks.shape[1]):
    print(f'Year: {year_string[i]}')

    for j in range(len(stocks.iloc[:,i])):
        tickerSymbol = stocks.iloc[j,i]
        # get data on this ticker
        tickerData = yf.Ticker(tickerSymbol)
        # get the historical prices for this ticker
        tickerDf = tickerData.history(period='1d', start=years[i][0], end=years[i][1])

        # only process data if there is data available -
        if tickerDf.shape[0] > 0:
            # save the data in the desired format                       # UPDATE HERE **********************************
            # save the date as a series
            # open = tickerDf.iloc[:,0]
            # high = tickerDf.iloc[:,1]
            # low = tickerDf.iloc[:, 2]
            close = tickerDf.iloc[:, 3]
            # volume = tickerDf.iloc[:, 4]

            # look up sector
            sector = None
            for k in range(sectors.shape[0]):
                if tickerSymbol == sectors.iloc[k, 1]:
                    sector = sectors.iloc[k, 2]

            # iterate through each day and create a list of data
            one_stock_list = []
            one_stock_list.append(tickerSymbol)
            one_stock_list.append(year_string[i])
            one_stock_list.append(election_code[i])
            one_stock_list.append(sector)

            norm = None
            volume_n = None
            print(f'Length of data: {len(tickerDf.iloc[:,0])}')
            for k in range(len(tickerDf.iloc[:,0])):
                # normalize the data based on closing of day 1
                if k == 0:
                    norm = close[k]                            # UPDATE HERE **********************************
                    # volume_n = volume[k]
                # accounts for any 0 norms - this is a function of getting bad data from the API
                if norm != 0:
                    # one_stock_list.append(volume[k]/norm)       # UPDATE HERE **********************************
                    one_stock_list.append(close[k])            # UPDATE HERE - NO NORMALIZATION ***************
                else:
                    one_stock_list.append(1)
            yearly_data.append(one_stock_list)
column_names = ['TICKER', 'YEAR', 'CODE', 'SECTOR']
for w in range(1,62):
    column_names.append(w)
new_df = pd.DataFrame(yearly_data)
new_df.set_axis(column_names, axis='columns', inplace=True)
new_df.to_csv(path)
