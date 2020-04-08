import copy
import math
import matplotlib.pyplot as plt


class Lloyd:
    def __init__(self, data, centers, threshold = 0.1):
        self.data = copy.deepcopy(data)
        self.centers = centers
        self.phi = [0] * len(self.data)     # contains the index of the center to which the point is assigned
        self.threshold = threshold
        self.historical_centers = []

        self.init_sets()
        t = math.inf
        while (t > self.threshold):
            self.cluster()
            t = self.adjust_centers()
        # self.plot_points()

    def compute_3means_cost(self):
        distance_squared = 0
        for i in range(len(self.data)):
            distance_squared += math.pow(self.get_distance(self.data[i][1:], self.centers[self.phi[i]]),2)
        return math.sqrt(distance_squared/len(self.data))

    def get_centers(self):
        return self.centers

    def adjust_centers(self):
        coordinates = [0.0] * len(self.data[0][1:])
        avg_coords = [[0.0 for j in range(len(self.data[0][1:]))] for j in range(len(self.centers))]
        total_center_assignments = [0] * len(self.centers)

        for i in range(len(self.data)):
            # keep track of total points assigned to each center
            total_center_assignments[self.phi[i]] += 1
            # get coordinate for point and add to total
            for k in range(1, len(self.data[0])):
                avg_coords[self.phi[i]][k-1] += self.data[i][k]

        # divide each coordinate by number assigned to center to get average
        for m in range(len(self.centers)):
            for n in range(len(self.data[0][1:])):
                avg_coords[m][n] = avg_coords[m][n] / total_center_assignments[m]

        # record largest distance between old and new centers and return this distance
        max_distance = 0
        for a in range(len(self.centers)):
            d = self.get_distance(self.centers[a], avg_coords[a])
            if d > max_distance:
                max_distance = d

        # record previous centers
        # assign avg_coords to self.centers
        self.historical_centers.append(self.centers)
        self.centers = copy.deepcopy(avg_coords)

        return max_distance

    def cluster(self):
        for i in range(len(self.data)):
            min_distance = math.inf
            center_index = None
            for j in range(len(self.centers)):
                # compute distance of x to all the centers and assign to center with minimum distance
                d = self.get_distance(self.data[i][1:], self.centers[j])
                if d < min_distance:
                    min_distance = d
                    center_index = j
            if center_index:
                self.phi[i] = center_index
            else:
                pass

    def get_distance(self, p1, p2):
        distance = 0
        # compute euclidean distance between two points
        # sum up the square of the distance between the two points (coordinate wise)
        for i in range(len(p1)):
            distance += math.pow((p1[i] - p2[i]), 2)
        return math.sqrt(distance)

    # plot the points AFTER the centers have been established
    def plot_points(self):
        index = 0
        color = ['r', 'b', 'g', 'm', 'b', 'g']
        x = []
        y = []
        x_center = []
        y_center = []
        txt = []
        txt_center = []
        # get list of points
        for i in range(len(self.data)):
            x.append(self.data[i][1])
            y.append(self.data[i][2])
        # Add list of point to plot
        fig, ax = plt.subplots()
        ax.scatter(x, y, color='cyan')
        # generate list of historical centers and add to plot
        for j in range(len(self.historical_centers)):
            x_center.clear()
            y_center.clear()
            for k in range(len(self.historical_centers[0])):
                x_center.append(self.historical_centers[j][k][0])
                y_center.append(self.historical_centers[j][k][1])
                txt_center.append(f"{self.historical_centers[j][k][0]:.3f}, {self.historical_centers[j][k][1]:.3f}")
                # txt_center.append(f"{self.historical_centers[j][k][0]:.0f}, {self.historical_centers[j][k][1]:.0f}")
            ax.scatter(x_center, y_center, color=color[index])
            index += 1

        plt.title(f"K-Means starting with output from Gonzalez (C2.txt)")
        round = 0
        for j, label in enumerate(txt_center):
            s = txt_center[j].split(',')
            round = int(j/3)
            ax.annotate(round, (float(s[0]), float(s[1])), size=10)
        plt.xlabel("x")
        plt.ylabel("y")
        plt.show()

    # get the dataset in a useful format with int/floats instead of strings and transform each x into a list
    def init_sets(self):
        # transform initial centers from points in data set to coordinates
        for k in range(len(self.centers)):
            self.centers[k] = self.data[self.centers[k]][1], self.data[self.centers[k]][2]


