# Copyright 2026 Joko Susilo
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
