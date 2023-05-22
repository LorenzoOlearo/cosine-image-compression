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
 
    
    
    
    
def main():
    signal = np.array([231, 32, 233, 161, 24, 71, 140, 245])
    cosine_signal = cosine_transform(signal)
    print(cosine_signal)
    print(dct(signal, norm='ortho'))
    
    

if __name__ == '__main__':
    main()
