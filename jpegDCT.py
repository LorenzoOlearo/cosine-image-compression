import numpy as np

def dct(vector):
    N = len(vector)
    cosine_vector = np.zeros(N)

    for k in range(N):
        for n in range(N):
            cosine_vector[k] += vector[n] * np.cos((np.pi * k * (2 * n + 1)) / (2 * N))
        
        if k == 0:
            scaling_factor = np.sqrt(1/N)
        else:
            scaling_factor = np.sqrt(2/N)
        
        cosine_vector[k] *= scaling_factor
            
    return cosine_vector


def idct(vector):
    N = len(vector)
    cosine_vector = np.zeros(N)
    
    for n in range(N):
        for k in range(N):
            if k == 0:
                scaling_factor = np.sqrt(1/N)
            else:
                scaling_factor = np.sqrt(2/N)
            
            cosine_vector[n] += scaling_factor * vector[k] * np.cos((np.pi * k * (2 * n + 1)) / (2 * N))
            
    return cosine_vector


def dct2(matrix):
    cosine_matrix = np.zeros(matrix.shape)

    for i in range(matrix.shape[0]):
        cosine_matrix[i] = dct(matrix[i])
    for i in range(matrix.shape[1]):
        cosine_matrix[:, i] = dct(cosine_matrix[:, i])

    return cosine_matrix


def idct2(matrix):
    cosine_matrix = np.zeros(matrix.shape)

    for i in range(matrix.shape[0]):
        cosine_matrix[i] = idct(matrix[i])
    for i in range(matrix.shape[1]):
        cosine_matrix[:, i] = idct(cosine_matrix[:, i])

    return cosine_matrix