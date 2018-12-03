from PIL import Image
import numpy as np
#import Image
import StringIO
from scipy import fftpack
import argparse
def dct_2d(image):
    return fftpack.dct(fftpack.dct(image.T, norm='ortho').T, norm='ortho')

def level_offset(data):
    return
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="path to the input image")
    parser.add_argument("output", help="path to the output image")
    args = parser.parse_args()

    input_file = args.input
    output_file = args.output
    with open(input_file, 'rb') as f:
        rawData = f.read()
    print(len(rawData))    
    if len(rawData) > 512*512:
        rawData = np.reshape(list(rawData),(512, 512,3))
        #image = Image.frombytes("RGB",(512, 512),rawData,decoder_name='raw')
        #ycbcr = image.convert('YCbCr')
        #rawData = np.array(ycbcr, dtype=np.uint8)
        #rawData = np.array(image, dtype=np.uint8)
    else:
        rawData = np.reshape(list(rawData),(512, 512))
    #print(len(rawData))
    #image = Image.open(input_file)
    #frombytes(mode, size, data, decorder_name, )
    #rawdata = np.reshape((rawData),(-1))
    
    #print(len(rawdata))
    
    with open(output_file, 'wb') as f:
        f.write(rawData)
    
    #
    #npmat = np.array(image, dtype=np.uint8)
    #print(help(image.getdata()))