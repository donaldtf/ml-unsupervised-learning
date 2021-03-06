from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from scipy.spatial.distance import cdist
import seaborn as sb
import pandas as pd
import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt
import math
import numpy as np
from kneed import KneeLocator

# https://towardsdatascience.com/feature-selection-with-pandas-e3690ad8504b
def plot_corr(name, x, y):
    x_copy = x.copy()
    x_copy['Target'] = y
    cor = x_copy.corr()
    
    # plt.figure()
    plt.figure(figsize=(12,10))
    plt.title('Feature Correlation Heat Map for {}'.format(name))
    plt.tight_layout()
    plt.autoscale()
    sb.heatmap(cor, annot=True, cmap=plt.cm.Reds)
    plt.savefig("features/{}.png".format(name), bbox_inches='tight')

# https://pythonprogramminglanguage.com/kmeans-elbow-method/
def get_optimal_k(name, X):
    # k means determine k
    distortions = []
    K = range(1,10)
    for k in K:
        kmeanModel = KMeans(n_clusters=k).fit(X)
        kmeanModel.fit(X)
        distortions.append(sum(np.min(cdist(X, kmeanModel.cluster_centers_, 'euclidean'), axis=1)) / X.shape[0])

    distortions = distortions / distortions[0]

    kneedle = KneeLocator(K, distortions, S=1.0, curve='convex', direction='decreasing')
    knee = math.floor(kneedle.knee)

    # Plot the elbow
    plt.figure()
    plt.plot(K, distortions, 'bx-')
    plt.axvline(x=knee, label="Selected K")
    plt.legend(loc="best")
    plt.xlabel('k')
    plt.ylabel('Normalized Average Distance')
    plt.title('Elbow Curve for {}'.format(name))
    plt.savefig("elbow_curves/{}.png".format(name))

    return knee

def kmeans(name, x, y):
    optimal_k = get_optimal_k(name, x)
    kmeans = KMeans(n_clusters=optimal_k, random_state=99).fit(x)

    labels = list(kmeans.labels_)

    encoded = pd.get_dummies(labels)
    plot_corr(name, encoded, y)

    print ("selected k for k means: " + str(optimal_k))

    return encoded

# https://scikit-learn.org/stable/auto_examples/mixture/plot_gmm_selection.html
def get_optimal_num_comps(name, X):
    # k means determine k
    bic = []
    K = range(1,10)
    for n_components in K:
        gmm = GaussianMixture(n_components=n_components)
        gmm.fit(X)
        bic.append(gmm.bic(X))

    kneedle = KneeLocator(K, bic, S=1.0, curve='convex', direction='decreasing')
    knee = math.floor(kneedle.knee)

    # Plot the elbow
    plt.figure()
    plt.plot(K, bic, 'bx-')
    plt.axvline(x=knee, label="Selected K")
    plt.legend(loc="best")
    plt.xlabel('k')
    plt.ylabel('BIC')
    plt.title('Elbow Curve for {}'.format(name))
    plt.savefig("elbow_curves/{}.png".format(name))

    return knee

# Credit to: https://github.com/cmaron/CS-7641-assignments/blob/master/assignment3/experiments/clustering.py
def gmm(name, x, y):
    n_components = get_optimal_num_comps(name, x)
    gmm = GaussianMixture(n_components=n_components)

    print ("selected n_components for gmm: " + str(n_components))

    gmm.fit(x)
    gmm_labels = gmm.predict(x)

    encoded = pd.get_dummies(gmm_labels)
    plot_corr(name, encoded, y)

    return encoded
