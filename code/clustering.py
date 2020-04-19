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
            y.append(mean(change) * X_SCALE)

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




# Plot the centers from pre and post
dr_post_x = [2.10774, 7.91684, 12.25591]
dr_post_y = [0.04020, -0.16921, -0.13397]

rd_post_x = [2.12747, 2.40553, 2.57121]
rd_post_y = [-2.05444, 2.08996, -6.26068]

rr_post_x = [0.62373, 0.70137, 3.43090]
rr_post_y = [0.53035, -0.58676, 0.23227]

dd_post_x = [1.27294, 3.69790, 5.07491]
dd_post_y = [0.02690, 0.34921, -2.15301]


dr_pre_x = [1.01867, 2.75602, 8.52695]
dr_pre_y = [0.20323, -0.44040, 0.60278]

rd_pre_x = [2.11375, 3.19218, 4.17244]
rd_pre_y = [0.65723, -3.23001, 5.09445]

rr_pre_x = [0.58195, 0.73613, 1.40148]
rr_pre_y = [0.66887, -0.83741 , 0.03691]

dd_pre_x = [0.85091, 2.15388, 3.68848]
dd_pre_y = [0.12771, 0.02961, -0.66893]




