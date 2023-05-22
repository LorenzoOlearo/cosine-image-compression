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



def check_cosine_transform(result):
    correct_cosine_signal = np.array([4.01e+02, 6.60e+00, 1.09e+02, -1.12e+02, 6.54e+01, 1.21e+02, 1.16e+02, 2.88e+01])
    print('Correct cosine signal: ', correct_cosine_signal)
    print('Result cosine signal: ', result)
    assert np.allclose(result, correct_cosine_signal, rtol=1e-2), 'cosine tranform missmatch'
 
    
    
def main():
    signal = np.array([231, 32, 233, 161, 24, 71, 140, 245])
    cosine_signal = cosine_transform(signal)
    
    check_cosine_transform(cosine_signal)
    print(cosine_signal)
    
    

if __name__ == '__main__':
    main()
