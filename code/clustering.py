import pandas as pd
from scipy import polyfit
import matplotlib.pyplot as plt
from statistics import mean
import Cluster_Lloyd

sectors = ['Financials', 'Materials', 'Consumer Staples', 'Industrials', 'Information Technology',
           'Consumer Discretionary', 'Energy', 'Health Care', 'Communication Services', 'Consumer Cyclical']

code = ['DR', 'RD', 'DD', 'RR']
code_label = ['Democrat to Republican', 'Republican to Democrat', 'Democrat to Democrat', 'Republican to Republican']
color = ['r', 'darkorange', 'yellow', 'palegreen', 'darkgreen', 'navy', 'skyblue', 'm', 'c', 'darkslategray']

X_SCALE = 100       # used to scale the x-axis / data (percent change)
Y_SCALE = 1000000000

# import the data
data = pd.read_csv("data\election_data_close_norm.csv")
raw_volume = pd.read_csv("data\election_data_volume_raw.csv")
raw_close = pd.read_csv("data\election_data_close_raw.csv")


# divide the data into four election segments
results = []

for i in range(len(code)):
    sector_x = []
    sector_y = []
    cluster_list = []
    count = 0
    for j in range(len(sectors)):
        # x and y used to store the points - x is used for average volume and y is used for average daily value change
        x = []
        y = []
        d = data[(data.CODE == code[i]) & (data.SECTOR == sectors[j])]  # query based on the code and sector
        v = raw_volume[(data.CODE == code[i]) & (data.SECTOR == sectors[j])]  # query based on the code and sector
        c = raw_close[(data.CODE == code[i]) & (data.SECTOR == sectors[j])]  # query based on the code and sector

        # plot the data and calculate the regression slope prior to election and after
        for k in range(5, 35):
            day_volume = v.iloc[:, k]
            day_close = c.iloc[:, k]
            if k == 5:
                previous_close = day_close
            else:
                previous_close = c.iloc[:, k-1]

            subtotal = 0
            change = []
            for index, value in day_volume.iteritems():
                # multiply volume by closing stock price
                subtotal += value * day_close[index]
                change.append((day_close[index] - previous_close[index]) / day_close[index])
            x.append(subtotal/Y_SCALE)   # divide by 1 billion for plotting / scaling purposes
            y.append(mean(change)* X_SCALE)

            if k == 34:
                # print('pause')
                pass
            # Used for clustering algorithm ################################################################
            cluster_list.append([count, subtotal/Y_SCALE, mean(change)* X_SCALE])
            count += 1
            ################################################################################################

        sector_x.append(x)
        sector_y.append(y)

    # plot the data for the category *****************************************************************************
    fig, ax = plt.subplots(1, figsize=(10, 5))
    fig.suptitle(code_label[i] + '- Pre Election')
    # plt.title('Pre Election')
    plt.xlabel('Daily Sector Volume in Dollars (Billions)')
    plt.ylabel('Daily Percent Change in Closing Value')
    # set the limits on the scales
    ax.set_xlim(0, 14)
    ax.set_ylim(-7.5, 7.5)
    # scatter plot of the data color coded by sector
    handles = []
    for z in range(len(sector_x)):
        handle = plt.scatter(sector_x[z], sector_y[z], s=15, c=color[z])
        handles.append(handle)



    # run clustering here ######################################################################
    # use cluster_list
    clusters = Cluster_Lloyd.Lloyd(cluster_list, [0, 1, 2], threshold=.3)

    # plot the centers in larger black circles
    c_x = []    # x points for cluster centers
    c_y = []    # y points for cluster centers
    formatted_centers = []   # used to store / display centers as text in the plot
    for v in range(len(clusters.centers)):
        c_x.append(clusters.centers[v][0])
        c_y.append(clusters.centers[v][1])
        formatted_centers.append(str(format(clusters.centers[v][0], '.5f') + ', ' + str(format(clusters.centers[v][1], '.5f') + ' ')))
    plt.scatter(c_x, c_y, c='black', s=50)
    print(f'Category: {code[i]}, Centers: {formatted_centers}')
    # display before and after slope as text in the plot
    plt.text(0, 1.01, 'Centers: ' + str(formatted_centers), transform=ax.transAxes)
    plt.legend(handles, sectors, ncol=3, loc='lower center', fontsize='small')
    plt.show()
