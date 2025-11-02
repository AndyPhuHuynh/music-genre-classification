import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

from src.dataset import Dataset

def plot_mfcc_pca(data: Dataset):
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(data.X)
    plt.scatter(X_pca[:, 0], X_pca[:, 1], c=data.y, cmap="tab10")
    plt.title("PCA projection of MFCC features")
    plt.show()