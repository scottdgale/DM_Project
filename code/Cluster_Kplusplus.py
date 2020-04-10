import copy
import math
import matplotlib.pyplot as plt
import random as rnd


class PlusPlus:
    def __init__(self, data, k=3):
        self.data = copy.deepcopy(data)
        self.k = k
        # self.init_sets()              # Used to get the data in list format
        self.centers = []
        self.squared_distances = [0.0] * len(self.data)

        # randomly choose the first center
        self.initial_index = 0
        self.centers.append(self.initial_index)
        self.phi = [self.initial_index] * len(self.data)
        self.cluster()
        # self.plot_points()

    def plot_probability(self):
        probability_list = []
        sub_total = 0.0
        for a in range(len(self.squared_distances)):
            sub_total += self.squared_distances[a]
            probability_list.append(sub_total)

        y = [0.5] * len(self.data)
        fig, ax = plt.subplots()
        ax.scatter(probability_list, y, marker='|')
        plt.title(f"Probability Distribution")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.show()

    def compute_3center_cost(self):
        max_distance = 0
        max_point = [0, 0]
        for i in range(len(self.data)):
            d = math.sqrt(self.get_distance(i, self.phi[i]))
            if d > max_distance:
                max_distance = d
                max_point = [i+1, self.phi[i]+1]

        return max_distance

    def compute_3means_cost(self):
        distance_squared = 0
        for i in range(len(self.data)):
            distance_squared += self.get_distance(i, self.phi[i])
        return math.sqrt(distance_squared/len(self.data))

    # plot the points AFTER the centers have been established
    def plot_points(self):
        x = []
        y = []
        x_center = []
        y_center = []
        txt = []
        txt_center = []
        # get array of centers and non-center data points
        for i in range(len(self.data)):
            if i in self.centers:
                x_center.append(self.data[i][1])
                y_center.append(self.data[i][2])
                txt_center.append(self.data[i][0])
            else:
                x.append(float(self.data[i][1]))
                y.append(float(self.data[i][2]))
                txt.append(self.data[i][0])
        fig, ax = plt.subplots()
        ax.scatter(x, y, color='cyan')
        ax.scatter(x_center, y_center, color='red')
        plt.title(f"K++ (C2.txt) with centers: {self.get_centers()}")
        for j, label in enumerate(txt_center):
            ax.annotate(label, (x_center[j], y_center[j]), size=14)
        plt.xlabel("x")
        plt.ylabel("y")
        plt.show()

    def get_centers(self):
        # adjust the centers for off by one error (add 1 to all values)
        print_centers = []
        for i in range(len(self.centers)):
            print_centers.append(self.centers[i] + 1)
        return print_centers

    def get_centers_index(self):
        # adjust the centers for off by one error (add 1 to all values)
        print_centers = []
        for i in range(len(self.centers)):
            print_centers.append(self.centers[i])
        return print_centers

    # run the K++ Algorithm
    def cluster(self):
        # iterate for each value of k (k = number of clusters)
        for i in range(1, self.k):
            running_total = 0
            new_center = None
            for j in range(len(self.data)):
                # calculate the distance between the point j and the current assigned center
                self.squared_distances[j] = self.get_distance(j, self.phi[j])
                running_total += self.squared_distances[j]

            for k in range(len(self.data)):
                self.squared_distances[k] = self.squared_distances[k] / running_total
            # total = sum(self.squared_distances)

            # generate a uniform random number [0,1]
            rand_num = rnd.random()
            # print(rand_num)
            probability = 0
            for a in range(1, len(self.data)):
                probability += self.squared_distances[a]
                if probability > rand_num:
                    # choose this value as the next center
                    new_center = a
                    break

            # add the new center to the mix
            self.centers.append(new_center)

            # update the mapping between points and centers
            for k in range(len(self.data)):
                # if distance between current assignment is > distance between new center - make new mapping
                if self.get_distance(k, self.phi[k]) > self.get_distance(k, new_center):
                    self.phi[k] = new_center
                    # calculate squared distances from centers

        return self.centers

    def get_distance(self, p1, p2):
        distance = 0
        # compute euclidean distance between two points
        # -1 compensates for off by 1 error (element 1 is in position 0)
        point_one = self.data[p1]
        point_two = self.data[p2]
        # sum up the square of the distance between the two points (coordinate wise)
        for i in range(1, len(point_one)):
            distance += math.pow((point_one[i] - point_two[i]), 2)
        return distance

    # get the dataset in a useful format with int/floats instead of strings and transform each x into a list
    def init_sets(self):
        for i in range(len(self.data)):
            self.data[i] = self.data[i].split()
            for j in range(0, len(self.data[i])):
                if j == 0:
                    self.data[i][j] = int(self.data[i][j])
                else:
                    self.data[i][j] = float(self.data[i][j])
