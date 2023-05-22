import numpy as np
import unittest
from scipy.fftpack import dct, idct


class TestCosineTransform():
    vector = np.array([231, 32, 233, 161, 24, 71, 140, 245])
    
    matrix = np.array([[231, 32, 233, 161, 24, 71, 140, 245],
                       [247, 40, 248, 245, 124, 204, 36, 107],
                       [234, 202, 245, 167, 9, 217, 239, 173],
                       [193, 190, 100, 167, 43, 180, 8, 70],
                       [11, 24, 210, 177, 81, 243, 8, 112],
                       [97, 195, 203, 47, 125, 114, 165, 181],
                       [193, 70, 174, 167, 41, 30, 127, 245],
                       [87, 149, 57, 192, 65, 129, 178, 228]])


    def check_cosine_transform_1D(self, result):
        scipy_cosine_vector = dct(self.vector, norm='ortho', type=2)
        assert np.allclose(result, scipy_cosine_vector, rtol=1e-3), 'Cosine tranform 1D missmatch'
        print('1D cosine tranform test passed!')


    def check_cosine_transform_2D(self, result):
        scipy_cosine_matrix = dct(dct(self.matrix.T, norm='ortho').T, norm='ortho')
        assert np.allclose(result, scipy_cosine_matrix, rtol=1e-3), 'Cosine tranform 2D missmatch'
        print('2D cosine tranform test passed!')
