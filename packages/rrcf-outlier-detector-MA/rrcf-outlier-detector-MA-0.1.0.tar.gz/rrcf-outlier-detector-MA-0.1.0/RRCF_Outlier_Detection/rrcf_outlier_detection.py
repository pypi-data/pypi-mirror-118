import pandas as pd
import numpy as np
import rrcf
from sklearn.preprocessing import StandardScaler


class Outlier_Detector:

    def __init__(self, x: np.array, num_trees: int, num_samples_per_tree: int):
        self.x = x
        self.num_trees = num_trees
        self.num_samples_per_tree = num_samples_per_tree
        self.forest = self.create_forest()

    def create_forest(self):
        n = self.x.shape[0]
        forest_size = n // self.num_samples_per_tree

        if self.num_trees <= 1:

            forest = rrcf.RCTree(self.x, index_labels=[i for i in range(n)])

        else:

            forest = []
            while len(forest) < self.num_trees:
                ixs = np.random.choice(n, size=(forest_size, self.num_samples_per_tree),
                                       replace=False)
                # Add sampled trees to forest
                trees = [rrcf.RCTree(self.x[ix, :], index_labels=ix) for ix in ixs]
                forest.extend(trees)

        return forest

    def rrcf_outlier_score(self):
        n = self.x.shape[0]

        if self.num_trees <= 1:

            avg_codisp = [self.forest.codisp(i) for i in [i for i in range(n)]]

        else:

            # Compute average CoDisp
            avg_codisp = pd.Series(0.0, index=np.arange(n))
            index = np.zeros(n)
            for tree in self.forest:
                codisp = pd.Series({leaf: tree.codisp(leaf)
                                    for leaf in tree.leaves})
                avg_codisp[codisp.index] += codisp
                np.add.at(index, codisp.index.values, 1)
            avg_codisp /= index

        return avg_codisp

    def rrcf_outlier_detector(self):
        n = self.x.shape[0]

        if self.num_trees <= 1:

            avg_codisp = [self.forest.codisp(i) for i in [i for i in range(n)]]

        else:

            # Compute average CoDisp
            avg_codisp = pd.Series(0.0, index=np.arange(n))
            index = np.zeros(n)
            for tree in self.forest:
                codisp = pd.Series({leaf: tree.codisp(leaf)
                                    for leaf in tree.leaves})
                avg_codisp[codisp.index] += codisp
                np.add.at(index, codisp.index.values, 1)
            avg_codisp /= index

        avg_codisp_std = np.absolute(StandardScaler().fit_transform(np.array(avg_codisp).reshape((-1, 1))))

        detected_outliers = self.x[(avg_codisp_std >= 3)[:,0],:]

        return detected_outliers