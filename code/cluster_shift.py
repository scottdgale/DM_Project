import matplotlib.pyplot as plt


sectors = ['Financials', 'Materials', 'Consumer Staples', 'Industrials', 'Information Technology',
           'Consumer Discretionary', 'Energy', 'Health Care', 'Communication Services', 'Consumer Cyclical']

code = ['DR', 'RD', 'RR', 'DD']
code_label = ['Democrat to Republican', 'Republican to Democrat', 'Republican to Republican', 'Democrat to Democrat']
color = ['r', 'darkorange', 'palegreen', 'navy']

x_pre = []
x_post = []
y_pre = []
y_post = []

# Plot the centers from pre and post
x_pre.append([1.01867, 2.75602, 8.52695])       # DR
y_pre.append([0.20323, -0.44040, 0.60278])

x_pre.append([2.11375, 3.19218, 4.17244])       # RD
y_pre.append([0.65723, -3.23001, 5.09445])

x_pre.append([0.58195, 0.73613, 1.40148])       # RR
y_pre.append([0.66887, -0.83741 , 0.03691])

x_pre.append([0.85091, 2.15388, 3.68848])       # DD
y_pre.append([0.12771, 0.02961, -0.66893])

x_post.append([2.10774, 7.91684, 12.25591])     # DR
y_post.append([0.04020, -0.16921, -0.13397])

x_post.append([2.12747, 2.40553, 2.57121])
y_post.append([-2.05444, 2.08996, -6.26068])

x_post.append([0.62373, 0.70137, 3.43090])
y_post.append([0.53035, -0.58676, 0.23227])

x_post.append([1.27294, 3.69790, 5.07491])
y_post.append([0.02690, 0.34921, -2.15301])

# setup the plot, axes, and labels
fig, ax = plt.subplots(1, figsize=(10, 5))
fig.suptitle('Shifting of Cluster Center by Category')
# plt.title('Pre Election')
plt.xlabel('Daily Sector Volume in Dollars (Billions)')
plt.ylabel('Daily Percent Change in Closing Value')
# set the limits on the scales
ax.set_xlim(0, 13)
ax.set_ylim(-6.5, 6.5)

handle = []
for i in range(len(code)):
    for k in range(3):
        # plot x_pre and x_post and draw a line (arrow) between the two
        plt.scatter(x_pre[i][k], y_pre[i][k], c=color[i], s=20)
        plt.scatter(x_post[i][k], y_post[i][k], c=color[i], s=0)

        # calculate the delta from pre to post
        dx = x_post[i][k] - x_pre[i][k]
        dy = y_post[i][k] - y_pre[i][k]

        if k == 0:
            handle.append(plt.arrow(x_pre[i][k], y_pre[i][k], dx, dy, linewidth=1.5, color=color[i], shape='full', head_width=.2))
        else:
            plt.arrow(x_pre[i][k], y_pre[i][k], dx, dy, linewidth=1.5, color=color[i], shape='full', head_width=.2)

plt.legend(handle, code_label, ncol=4, loc='upper center', fontsize='small')
plt.show()
