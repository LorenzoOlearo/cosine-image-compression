import argparse

from cosineimagecompression import CosineImageCompression



def main():
    parser = argparse.ArgumentParser(description='Cosine Image Compression.  Written by Lorenzo Olearo and Alessandro Riva, 2023')
    parser.add_argument('--nogui', action='store_true', help='Run program with no GUI', default=False)
    parser.add_argument('--test', action='store_true', help='Run test')
    parser.add_argument('--performance', action='store_true', help='Run performance test') 
    
    parser.add_argument('--slow', action='store_true', help='Use direct cosine transform instead of fast cosine transform', default=False)
    
    parser.add_argument('--order', action='store_true', help='Test DCT on matrix on order of 2 size matrices', default=False)
    parser.add_argument('--incremental', action='store_true', help='Test DCT on matrix on incremental size matrices', default=False)
    
    parser.add_argument('--lower', type=int, help='Lower bound for performance tests', default=2)
    parser.add_argument('--upper', type=int, help='Upper bound for performance tests', default=8)
    parser.add_argument('--iterations', type=int, help='Iteration of the same tests', default=1)
    parser.add_argument('--load', action='store_true', help='Load pre-computed data in order to redraw plots', default=False)
    
    args = parser.parse_args()
    
    CosineImageCompression(args)
   
    

if __name__ == '__main__':
    main()
