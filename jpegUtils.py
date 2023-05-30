import numpy as np
import scipy.fftpack as fft


def extract_macro_blocks(image, macro_size):
    macro_blocks = np.zeros((image.shape[0] // macro_size, image.shape[1] // macro_size, macro_size, macro_size))
    
    for i in range(macro_blocks.shape[0]):
        for j in range(macro_blocks.shape[1]):
            macro_blocks[i, j] = image[i * macro_size : (i + 1) * macro_size, j * macro_size : (j + 1) * macro_size]
            
    return macro_blocks



def bitmap_to_jpeg(bitmap, macro_size, freq_cut, fast = True):
    bitmap = bitmap - 128
    macro_blocks = extract_macro_blocks(bitmap, macro_size)
    dct_macro_blocks = np.zeros(macro_blocks.shape)

    for i in range(macro_blocks.shape[0]):
        for j in range(macro_blocks.shape[1]):
            if fast == True:
                dct_macro_blocks[i, j] = jpegDCT.dct2(macro_blocks[i, j])
            else:
                dct_macro_blocks[i, j] = fft.dct(fft.dct(macro_blocks[i, j], norm = 'ortho'), norm = 'ortho')