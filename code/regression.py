import pandas as pd
from scipy import polyfit
import matplotlib.pyplot as plt

sectors = ['Financials', 'Materials', 'Consumer Staples', 'Industrials', 'Information Technology',
           'Consumer Discretionary', 'Energy', 'Health Care', 'Communication Services', 'Consumer Cyclical']

code = ['DR', 'RD', 'DD', 'RR']
code_label = ['Democrat to Republican', 'Republican to Democrat', 'Democrat to Democrat', 'Republican to Republican']

# import the data
data = pd.read_csv("data\election_data_close_norm.csv")

# divide the data into four election segments
results = []

for i in range (len(code)):

    for j in range(len(sectors)):
        # x and y are lists used to store the points - x is used for days and y is used for norm stock close
        x = []
        y = []
        d = data[(data.CODE == code[i]) & (data.SECTOR == sectors[j])]

        # plot the data and calculate the regression slope prior to election and after
        for k in range(5, 65):
            day = d.iloc[:, k]
            for value in day.iteritems():
                y.append(value[1])
                x.append(k-35)

        # plot the data ********************************************************************************
        fig, ax = plt.subplots(1, figsize=(10,5))
        fig.suptitle(code_label[i])
        plt.xlabel('Days prior to and after the election (0 is election)')
        plt.ylabel(sectors[j])

        # scatter plot of the data
        plt.scatter(x, y, s=15, c="blue")

        # calculate the slope for j sector within i code
        # break the data in half (prior to election and after the election)
        x_prior = x[:int(len(x)/2)]
        y_prior = y[:int(len(x)/2)]
        x_after = x[int(len(x)/2):]
        y_after = y[int(len(x)/2):]

        slope_prior, intercept_prior = polyfit(x_prior, y_prior, 1)
        slope_after, intercept_after = polyfit(x_after, y_after, 1)

        # generate the points for two lines (before and after)
        line_x = [-30, 0, 30]
        line_y = [1, intercept_prior, slope_after*30 + intercept_after]

        plt.plot(line_x, line_y, linewidth=2.0, c='red')

        # plot a dashed line along x=0 to represent the election
        plt.plot([0,0],[0.5,2] , linewidth=1.0, c='black', linestyle=':')

        # display before and after slope as text in the plot
        plt.text(-20, 1.8, 'Slope prior: ' + str(format(slope_prior, '.5f')))
        plt.text(10, 1.8, 'Slope after: ' + str(format(slope_after, '.5f')))

        plt.show()

        results.append([code[i], sectors[j], slope_prior, slope_after])
        print(f"Category: {code[i]}, Sector: {sectors[j]}, Slope: {slope_prior}")








