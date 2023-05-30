import numpy as np
import scipy.fftpack as fft

import jpegDCT



def extract_macro_blocks(image, macro_size):
    macro_blocks = np.zeros((image.shape[0] // macro_size, image.shape[1] // macro_size, macro_size, macro_size))
    
    for i in range(macro_blocks.shape[0]):
        for j in range(macro_blocks.shape[1]):
            macro_blocks[i, j] = image[i * macro_size : (i + 1) * macro_size, j * macro_size : (j + 1) * macro_size]
            
    return macro_blocks



def frequency_cut(macro_block, freq_cut):
    for i in range(macro_block.shape[0]):
        for j in range(macro_block.shape[1]):
            if i + j >= freq_cut:
                macro_block[i, j] = 0
                
    return macro_block



def clamp_macro_block(macro_block):
    clamped_macro_block = np.round(macro_block) 
    clamped_macro_block = np.clip(macro_block, 0, 255)
    
    return clamped_macro_block



def dct2(macro_block, fast):
    if fast == False:
        dct_macro_block = jpegDCT.dct2(macro_block)
    else:
        dct_macro_block = fft.dct(fft.dct(macro_block, axis=0, norm='ortho'), axis=1, norm='ortho')
    
    return dct_macro_block



def idct2(dct_macro_block, fast):
    if fast == False:
        macro_block = jpegDCT.idct2(dct_macro_block)
    else:
        macro_block = fft.idct(fft.idct(dct_macro_block, axis=0, norm='ortho'), axis=1, norm='ortho')
        
    return macro_block
    


def macro_block_compression(macro_block, freq_cut, fast):
    macro_block = dct2(macro_block, fast)
    macro_block = frequency_cut(macro_block, freq_cut) 
    macro_block = idct2(macro_block, fast)
    macro_block = clamp_macro_block(macro_block)
    
    return macro_block



def recompose_macro_blocks(macro_blocks):
    image = np.zeros((macro_blocks.shape[0] * macro_blocks.shape[2], macro_blocks.shape[1] * macro_blocks.shape[3]))
    
    for i in range(macro_blocks.shape[0]):
        for j in range(macro_blocks.shape[1]):
            image[i * macro_blocks.shape[2] : (i + 1) * macro_blocks.shape[2], j * macro_blocks.shape[3] : (j + 1) * macro_blocks.shape[3]] = macro_blocks[i, j]
            
    return image



def bitmap_to_jpeg(bitmap, macro_size, freq_cut, fast = True):
    macro_blocks = extract_macro_blocks(bitmap, macro_size)
    compressed_macro_blocks = np.zeros(macro_blocks.shape)

    for i in range(macro_blocks.shape[0]):
        for j in range(macro_blocks.shape[1]):
            compressed_macro_blocks[i, j] = macro_block_compression(macro_blocks[i, j], freq_cut, fast)
            
    return recompose_macro_blocks(compressed_macro_blocks)
            