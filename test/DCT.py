import numpy as np
import scipy.fftpack as fftpack
import os
from PIL import Image
import matplotlib.pyplot as plt

import jpegDCT
import jpegUtils



class TestCosineTransform():

    def __init__(self):
        self.vector = np.array([231, 32, 233, 161, 24, 71, 140, 245])

        self.matrix = np.array([[231, 32, 233, 161, 24, 71, 140, 245],
                                [247, 40, 248, 245, 124, 204, 36, 107],
                                [234, 202, 245, 167, 9, 217, 239, 173],
                                [193, 190, 100, 167, 43, 180, 8, 70],
                                [11, 24, 210, 177, 81, 243, 8, 112],
                                [97, 195, 203, 47, 125, 114, 165, 181],
                                [193, 70, 174, 167, 41, 30, 127, 245],
                                [87, 149, 57, 192, 65, 129, 178, 228]])
        
        # Load a test bitmap image
        self.bitmap = Image.open(os.path.join(os.path.dirname(__file__), 'images', 'deer.bmp')).convert('L')
        self.bitmap = np.array(self.bitmap)
                             
                             

    def run_test(self):
        cosine_vector = jpegDCT.dct(self.vector)
        cosine_matrix = jpegDCT.dct2(self.matrix)

        self.check_cosine_transform_1D(cosine_vector)
        self.check_cosine_transform_2D(cosine_matrix)
        self.check_cosine_anti_transform_1D(jpegDCT.idct(cosine_vector))
        self.check_cosine_anti_transform_2D(jpegDCT.idct2(cosine_matrix))
       
        compressed = jpegUtils.bitmap_to_jpeg(self.bitmap, macro_size=8, freq_cut=2, fast=True)
        plt.imshow(compressed, cmap=plt.cm.gray)
        plt.show()



    def check_cosine_transform_1D(self, result):
        scipy_cosine_vector = fftpack.dct(self.vector, norm='ortho', type=2)
        assert np.allclose(result, scipy_cosine_vector, rtol=1e-3), 'Cosine tranform 1D missmatch'
        print('1D cosine tranform test passed!')



    def check_cosine_transform_2D(self, result):
        scipy_cosine_matrix = fftpack.dct(fftpack.dct(self.matrix, axis=0, norm='ortho'), axis=1, norm='ortho')
        assert np.allclose(result, scipy_cosine_matrix, rtol=1e-3), 'Cosine tranform 2D missmatch'
        print('2D cosine tranform test passed!')



    def check_cosine_anti_transform_1D(self, result):
        assert np.allclose(result, self.vector, rtol=1e-3), 'Cosine anti tranform 1D missmatch'
        print('1D cosine anti tranform test passed!')



    def check_cosine_anti_transform_2D(self, result):
        assert np.allclose(result, self.matrix, rtol=1e-3), 'Cosine anti tranform 2D missmatch'
        print('2D cosine anti tranform test passed!')
