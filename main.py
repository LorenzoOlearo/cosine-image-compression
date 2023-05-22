import numpy as np
from scipy.fftpack import dct, idct


def cosine_transform(signal):
    N = len(signal)
    cosine_signal = np.zeros(N)

    for k in range(N):
        for n in range(N):
            cosine_signal[k] += signal[n] * np.cos((np.pi * k * (2 * n + 1)) / (2 * N))
        
        if k == 0:
            scaling_factor = np.sqrt(1/N)
        else:
            scaling_factor = np.sqrt(2/N)
        
        cosine_signal[k] *= scaling_factor
            
    return cosine_signal


def cosine_transform_matrix(matrix):
    cosine_matrix = np.zeros(matrix.shape)

    for i in range(matrix.shape[0]):
        cosine_matrix[i] = cosine_transform(matrix[i])
    for i in range(matrix.shape[1]):
        cosine_matrix[:, i] = cosine_transform(cosine_matrix[:, i])

    return cosine_matrix


    
def main():
    signal = np.array([231, 32, 233, 161, 24, 71, 140, 245])
    cosine_signal = cosine_transform(signal)
    print('DCT 1D:\n', cosine_signal)

    matrix = np.array([[231, 32, 233, 161, 24, 71, 140, 245],
                       [247, 40, 248, 245, 124, 204, 36, 107],
                       [234, 202, 245, 167, 9, 217, 239, 173],
                       [193, 190, 100, 167, 43, 180, 8, 70],
                       [11, 24, 210, 177, 81, 243, 8, 112],
                       [97, 195, 203, 47, 125, 114, 165, 181],
                       [193, 70, 174, 167, 41, 30, 127, 245],
                       [87, 149, 57, 192, 65, 129, 178, 228]])

    cosine_matrix = cosine_transform_matrix(matrix)
    print('DCT 2D:\n', cosine_matrix)


    

if __name__ == '__main__':
    main()
