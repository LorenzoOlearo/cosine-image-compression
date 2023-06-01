import numpy as np
import pandas as pd
import scipy.fftpack as fftpack
import matplotlib.pyplot as plt
import seaborn as sns
import time
import os

import jpegDCT



def compute_dct(matrix):
    start = time.time()
    jpegDCT.dct2(matrix)
    end = time.time()
    elapsed = end - start
    
    return elapsed
   
    
    
def compute_fdct(matrix):
    start = time.time()
    fftpack.dct(fftpack.dct(matrix, axis=0, norm='ortho'), axis=1, norm='ortho')
    end = time.time()
    elapsed = end - start
    
    return elapsed
    


def benchmark_matrices(lower, upper, i):
    sizes = list(range(lower, upper + 1))
    elapsed_direct = []
    elapsed_fast = []
    
    for size in sizes:
        matrix = (np.random.random((size, size)) * 255).astype(int)
        elapsed_direct += [compute_dct(matrix)]
        elapsed_fast += [compute_fdct(matrix)]
        
    
    benchmark_data = pd.DataFrame({'size': sizes,
                                   'direct': elapsed_direct,
                                   'fast': elapsed_fast})
    
    make_plots(benchmark_data, i)
        
    
        
       
        
def make_plots(benchmark_data, i):
    benchmark_data = benchmark_data.melt(id_vars='size', value_vars=['direct', 'fast'], var_name='y_type', value_name='time')

    sns.barplot(data=benchmark_data, x='size', y='time', hue='y_type', errorbar=None, palette='hls').set_yscale('log')
    plt.tight_layout()
    # plt.show()
    
    plt.savefig(os.path.join(os.getcwd(), 'test', 'benchmark-results', 'bench-' + str(i)))
    plt.clf()

    
    
        
        
        
def run_test(lower=2, upper=20, iterations=10):
    for i in range(iterations):
        benchmark_matrices(lower, upper, i)
    
    
        
        
        