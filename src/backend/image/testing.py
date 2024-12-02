import numpy as np

def calculate_eigendecomposition(C):
    n = len(C)
    eigenvalues = np.zeros(n)
    eigenvectors = np.zeros((n, n))
    
    C_remaining = np.array(C)
    
    for i in range(10):
        print(f"Calculating eigenvector {i+1}")
        v = np.random.rand(n)
        v = v / np.linalg.norm(v)
        
        for _ in range(100):
            Cv = np.dot(C_remaining, v)
            lambda_i = np.dot(v, Cv) / np.dot(v, v)
            
            v_new = Cv / np.linalg.norm(Cv)
            
            if np.allclose(v, v_new, rtol=1e-6):
                break
            v = v_new
            
        eigenvalues[i] = lambda_i
        eigenvectors[:, i] = v
        
        C_remaining = C_remaining - lambda_i * np.outer(v, v)
    
    idx = eigenvalues.argsort()[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]
    
    return eigenvectors, eigenvalues