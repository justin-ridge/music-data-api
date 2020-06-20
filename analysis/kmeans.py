import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})


def kmeans_cluster(features):
    clustering_kmeans = KMeans(n_clusters=5)
    features['cluster'] = clustering_kmeans.fit_predict(features)
    return features


def pca_reduce(features):
    reduced_data = PCA(n_components=2).fit_transform(features)
    results = pd.DataFrame(reduced_data, columns=['pca1', 'pca2'])
    return results


def plot_kmeans_cluster(features, results):
    sns_plot = sns.scatterplot(
        x="pca1", y="pca2", hue=features['cluster'], data=results).get_figure()
    sns_plot.savefig("kmeans_cluster.png")
    plt.title('K-means Clustering with 2 dimensions')
    plt.show()


def plot_kmeans_target(labels, results):
    sns_plot = sns.scatterplot(
        x="pca1", y="pca2", hue=labels['target'], data=results).get_figure()
    sns_plot.savefig("kmeans_cluster_target.png")
    plt.title('K-means Clustering with 2 dimensions')
    plt.show()


def plot_cluster(cluster, combined):
    c0 = combined[combined['cluster'] == cluster]
    c0 = c0.drop(['cluster'], axis=1)
    plot_cluster_mean(c0, cluster)
    plot_cluster_attributes(c0, cluster)
    plot_cluster_genre(c0, cluster)


def plot_cluster_mean(c0, cluster):
    c0fig = c0.mean().plot(kind='barh', figsize=(20, 16), fontsize=26).get_figure()
    c0fig.savefig('c' + str(cluster) + '_bar.png')


def plot_cluster_attributes(c0, cluster):
    c0f = c0.drop(['genre_A Capella', 'genre_Alternative', 'genre_Anime', 'genre_Blues',
                   'genre_Childrens Music', 'genre_Classical', 'genre_Comedy',
                   'genre_Country', 'genre_Dance', 'genre_Electronic', 'genre_Folk',
                   'genre_Hip-Hop', 'genre_Indie', 'genre_Jazz', 'genre_Movie',
                   'genre_Opera', 'genre_Pop', 'genre_R&B', 'genre_Rap', 'genre_Reggae',
                   'genre_Reggaeton', 'genre_Rock', 'genre_Ska', 'genre_Soul',
                   'genre_Soundtrack', 'genre_World', 'target', 'duration_ms'], axis=1)
    c0ffig = c0f.mean().plot(kind='pie', figsize=(20, 16), fontsize=26).get_figure()
    c0ffig.savefig('c' + str(cluster) + '_pie.png')


def plot_cluster_genre(c0, cluster):
    c0g = c0.drop(['acousticness', 'danceability', 'duration_ms', 'energy',
                   'instrumentalness', 'liveness', 'loudness', 'speechiness', 'valence', 'target'], axis=1)
    c0gfig = c0g.mean().plot(kind='pie', figsize=(20, 16), fontsize=26).get_figure()
    c0gfig.savefig('c' + str(cluster) + '_pie_genre.png')


def create_plots():
    features = pd.read_csv('features.csv', index_col=0)
    labels = pd.read_csv('labels.csv', index_col=0)
    features = kmeans_cluster(features)
    results = pca_reduce(features)
    plot_kmeans_cluster(features, results)
    plot_kmeans_target(labels, results)
    combined = features
    combined['target'] = labels['target']
    for i in range(5):
        plot_cluster(i, combined)


create_plots()
