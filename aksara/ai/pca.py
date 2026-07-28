import numpy as np

def pca(data, n_components=2):
    """PCA dimensionality reduction dengan NumPy"""
    data = np.array(data)
    
    # Center data
    data = data - np.mean(data, axis=0)
    
    # Covariance matrix
    cov = np.cov(data.T)
    
    # Eigenvalues & eigenvectors
    eigenval, eigenvec = np.linalg.eig(cov)
    
    # Sort
    idx = np.argsort(eigenval)[::-1]
    eigenvec = eigenvec[:, idx]
    
    # Project
    return np.dot(data, eigenvec[:, :n_components]).tolist()
