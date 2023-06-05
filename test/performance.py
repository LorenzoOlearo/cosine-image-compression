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



def benchmark_order_matrices(lower, upper, i, load):
    if load:
        benchmark_data = pd.read_csv(os.path.join(os.getcwd(), 'test', 'benchmark-order-results-' + str(i) + '.csv'))
    else:
        sizes = list(range(lower, upper + 1))
        elapsed_direct = []
        elapsed_fast = []
        
        for size in sizes:
            matrix = (np.random.random((2 ** size, 2 ** size)) * 255).astype(int)
            print('(order) Computing: 2^' + str(size))
            elapsed_direct  += [compute_dct(matrix)]
            elapsed_fast    += [compute_fdct(matrix)]
            
        benchmark_data = pd.DataFrame({'size': sizes,
                                       'direct': elapsed_direct,
                                       'fast': elapsed_fast})

        benchmark_data.to_csv(os.path.join(os.getcwd(), 'test', 'benchmark-order-results-' + str(i) + '.csv'))

    plot_order_results(benchmark_data, i)



def benchmark_incremental_matrices(lower, upper, i, load):
    if load:
        benchmark_data = pd.read_csv(os.path.join(os.getcwd(), 'test', 'benchmark-incremental-results-' + str(i) + '.csv'))
    else:
        sizes = list(range(2 ** lower, (2 ** (upper - 1) + 1)))
        elapsed_direct = []
        elapsed_fast = []

        for size in sizes:
            matrix = (np.random.random((size, size)) * 255).astype(int)
            print('(incremental) Computing: ' + str(size))
            elapsed_direct  += [compute_dct(matrix)]
            elapsed_fast    += [compute_fdct(matrix)]

        benchmark_data = pd.DataFrame({'size': sizes,
                                       'direct': elapsed_direct,
                                       'fast': elapsed_fast})

        benchmark_data.to_csv(os.path.join(os.getcwd(), 'test', 'benchmark-incremental-results-' + str(i) + '.csv'))

    plot_incremental_results(benchmark_data, i)



def plot_order_results(benchmark_data, i):
    result_path = os.path.join(os.getcwd(), 'test', 'benchmark-results')
    benchmark_data.to_csv(os.path.join(result_path, 'bench-order-' + str(i) + '.csv'))

    benchmark_data = benchmark_data.melt(id_vars='size', value_vars=['direct', 'fast'], var_name='y_type', value_name='time')

    sns.barplot(data=benchmark_data, x='size', y='time', hue='y_type', errorbar=None, palette='hls').set_yscale('log')
    plt.tight_layout()

    plt.savefig(os.path.join(result_path, 'bench-order-' + str(i)))
    plt.clf()



def plot_incremental_results(benchmark_data, i):
    result_path = os.path.join(os.getcwd(), 'test', 'benchmark-results')
    benchmark_data.to_csv(os.path.join(result_path, 'bench-incremental-' + str(i) + '.csv'))

    benchmark_data = benchmark_data.melt(id_vars='size', value_vars=['direct', 'fast'], var_name='y_type', value_name='time')

    sns.lineplot(data=benchmark_data, x='size', y='time', hue='y_type', errorbar=None, palette='hls').set_yscale('log')
    plt.tight_layout()

    plt.savefig(os.path.join(result_path, 'bench-incremental-' + str(i)))
    plt.clf()


        
def run_test(iterations=1, lower=1, upper=8, order=True, incremental=True, load=False):
    for i in range(iterations):
        if order:
            benchmark_order_matrices(lower, upper, i, load)
        
        if incremental:
            benchmark_incremental_matrices(lower, upper, i, load)
