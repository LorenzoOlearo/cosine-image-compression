import numpy as np
from scipy.fftpack import dct, idct

from test import TestCosineTransform

from cosineimagecompression import CosineImageCompression
    
def main():
#    vector = np.array([231, 32, 233, 161, 24, 71, 140, 245])
#    matrix = np.array([[231, 32, 233, 161, 24, 71, 140, 245],
#                       [247, 40, 248, 245, 124, 204, 36, 107],
#                       [234, 202, 245, 167, 9, 217, 239, 173],
#                       [193, 190, 100, 167, 43, 180, 8, 70],
#                       [11, 24, 210, 177, 81, 243, 8, 112],
#                       [97, 195, 203, 47, 125, 114, 165, 181],
#                       [193, 70, 174, 167, 41, 30, 127, 245],
#                       [87, 149, 57, 192, 65, 129, 178, 228]])
#
#    cosine_vector = cosine_transform(vector)
#    cosine_matrix = cosine_transform_matrix(matrix)
#
#    test = TestCosineTransform()
#    test.check_cosine_transform_1D(cosine_vector)
#    test.check_cosine_transform_2D(cosine_matrix)
    
    CosineImageCompression()

    

if __name__ == '__main__':
    main()