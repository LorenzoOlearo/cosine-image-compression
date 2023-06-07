import argparse

from cosineimagecompression import CosineImageCompression



def main():
    parser = argparse.ArgumentParser(description='Cosine Image Compression')
    parser.add_argument('--nogui', action='store_true', help='Run program with no GUI', default=False)
    parser.add_argument('--test', action='store_true', help='Run test')
    parser.add_argument('--performance', action='store_true', help='Run performance test') 
    args = parser.parse_args()
    
    CosineImageCompression(args)
   
    

if __name__ == '__main__':
    main()
