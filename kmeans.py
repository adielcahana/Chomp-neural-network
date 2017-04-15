import winboard, training, neuralNet
import numpy as np
import random
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as mpatches
import pickle


#########################################################################################
class Cluster:
    def __init__(self, centroid, clusterCollection):
        self._centroid = centroid
        self._last_centroid = centroid + 1
        self._data = []
        self._clusterCollection = clusterCollection

    def update(self):
        self._last_centroid = self._centroid
        self._centroid = np.mean(self._data, axis=0)
        if self.stop():
            self._clusterCollection.stop[self._clusterCollection.data.index(self)] = 1
        self._data = []

    def add(self, x):
        self._data.append(x)

    def stop(self):
        return np.all(np.absolute((self._centroid - self._last_centroid)) == 0)

    def __len__(self):
        return len(self._data)

#########################################################################################
class ClusterCollection:
    def __init__(self, k):
        self.data = []
        self.stop = np.zeros(k)
        self.k = k

    def __iter__(self):
        return iter(self.data)

    def sholdStop(self):
        if np.sum(self.stop) == self.k:
            return True
        else:
            self.stop = np.zeros(self.k)
            return False

    def add(self, cluster):
        self.data.append(cluster)

    def get(self, index):
        return self.data[index]

    def plot(self, filePath):
        fig = plt.figure(tight_layout=True)
        patches = []
        ax = fig.add_subplot(111, projection='3d')
        for cluster in self.data:
            z, x, y = [], [], []
            for row in cluster._data:
                x.append(row[0])
                y.append(row[1])
                z.append(row[2])
            ax.scatter(x, y, z, zdir='z', c=cluster._color)
            # ax.scatter(cluster._centroid[0], cluster._centroid[1], cluster._centroid[2], zdir='z', s=50, c='red')
            patches.append(mpatches.Patch(color=cluster._color))

        ax.legend(handles=patches)
        # Put a legend to the right of the current axis
        # ax.legend(bbox_to_anchor=(1.3, 0.5))

        if filePath == None:
            fig.show()
        else:
            fig.savefig(filePath)


#########################################################################################
class Kmeans:
    def distance(self, pointA, pointB):
        return np.sqrt(np.sum((pointA - pointB) ** 2))

    def assignment(self, data, k, trueboards, falseboards, nn):
        clusters = ClusterCollection(k)
        # temp_board = training.initial_board(8, 8)
        # winboard.detranslate(random.choice(trueboards), temp_board)
        # clusters.add(Cluster(np.array(nn.translate(temp_board)), clusters))
        # temp_board = training.initial_board(8, 8)
        # winboard.detranslate(random.choice(falseboards), temp_board)
        # clusters.add(Cluster(np.array(nn.translate(temp_board)), clusters))
        for i in range(k):
            clusters.add(Cluster(random.choice(data), clusters))
        self.partition(data, clusters)
        return clusters

    def partition(self, data, clusters):
        for board in data:
            min = self.distance(board, clusters.get(0)._centroid)
            min_clust = clusters.get(0)
            for cluster in clusters:
                dist = self.distance(board, cluster._centroid)
                if dist < min:
                    min = dist
                    min_clust = cluster
            min_clust.add(board)

    def oneIter(self, data, clusters):
        for cluster in clusters:
            cluster.update()
        self.partition(data, clusters)


#########################################################################################
def main():

    with open('true.pickle', 'rb') as fp:
        trueboard = list(pickle.load(fp))
    with open('false.pickle', 'rb') as fp:
        falseboard = list(pickle.load(fp))

    print(len(trueboard), len(falseboard))
    nn = neuralNet.NeuralNet(0,0,0,0)
    data = []
    for board in trueboard:
        temp_board = training.initial_board(8, 8)
        winboard.detranslate(board, temp_board)
        data.append(np.array(nn.translate(temp_board)))

    for board in falseboard:
        temp_board = training.initial_board(8, 8)
        winboard.detranslate(board, temp_board)
        data.append(np.array(nn.translate(temp_board)))

    print(len(data))
    data = np.array(data)
    k = 2
    km = Kmeans()
    clusters = km.assignment(data, k, trueboard, falseboard, nn)

    i = 0
    while not clusters.sholdStop():
        km.oneIter(data, clusters)
        print("iter num " + str(i))
        # if i%10 == 0:
        #     clusters.plot("C:/Users/Adiel/Desktop/figures/" + "fig_" + str(i) + ".png")
        i += 1

    pickle.dump(clusters, open("clusters.pickle", "wb"))
    for cluster in clusters:
        print(len(cluster))

main()






