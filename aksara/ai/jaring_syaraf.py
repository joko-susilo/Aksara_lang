import numpy as np

def jaring_syaraf(X, y, hidden=3, iterasi=100):
    """Neural network sederhana 1 hidden layer"""
    X = np.array(X)
    y = np.array(y).reshape(-1, 1)
    
    n_input = X.shape[1]
    
    # Inisialisasi bobot
    np.random.seed(0)
    W1 = np.random.randn(n_input, hidden) * 0.01
    b1 = np.zeros((1, hidden))
    W2 = np.random.randn(hidden, 1) * 0.01
    b2 = np.zeros((1, 1))
    
    for _ in range(iterasi):
        # Forward
        z1 = X @ W1 + b1
        a1 = np.maximum(0, z1)  # ReLU
        z2 = a1 @ W2 + b2
        
        # Loss (MSE)
        loss = np.mean((z2 - y)**2)
        
        # Backprop sederhana
        dz2 = z2 - y
        dW2 = a1.T @ dz2 / len(X)
        db2 = np.mean(dz2)
        
        dz1 = dz2 @ W2.T
        dz1[z1 <= 0] = 0
        dW1 = X.T @ dz1 / len(X)
        db1 = np.mean(dz1)
        
        # Update
        laju = 0.01
        W1 -= laju * dW1
        b1 -= laju * db1
        W2 -= laju * dW2
        b2 -= laju * db2
    
    return {"W1": W1.tolist(), "b1": b1.tolist(), "W2": W2.tolist(), "b2": b2.tolist()}
