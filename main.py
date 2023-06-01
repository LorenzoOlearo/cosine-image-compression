from cosineimagecompression import CosineImageCompression
from test.DCT import TestCosineTransform
from test.performance import run_test
from gui import GUI

def main():
    TestCosineTransform().run_test()
    CosineImageCompression()
    run_test()
    

if __name__ == '__main__':
    main()
