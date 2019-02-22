# coding=utf8
""" 
demonstrate how to use jpeg codec
calculate PSNR

Student ID: 107522049
Author: Cheng-Hsin Wang
Country: ROC
School: NCU 
"""
from jpeg.codec import Encoder, Decoder
from jpeg.bitio import BitWriter, BitReader
import argparse
import contextlib
import numpy as np
import math
import os
from scipy import fftpack 
    
    
def MSE(image1,image2,bpp):
    sum = 0
    for linex,liney in zip(image1,image2):
        for pixelx,pixely in zip(linex,liney):
            for datax,datay in zip(pixelx,pixely):
                sum += (datax - datay) ** 2 
    return sum/512/512/bpp
    
def PSNR(mse):
    return 20*math.log(255/math.sqrt(mse),10)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", help="-c compress , -d decompress, -psnr")
    parser.add_argument("bpp", help="-n byte per pixel")
    parser.add_argument("QF", help="-n byte per pixel")
    parser.add_argument("file", help="path to the input image")
    args = parser.parse_args()
    inputFile = args.file.split("\r")[0]
    mode = args.mode
    bpp = args.bpp
    QF = int(args.QF)
    dirname = inputFile.split(".")[0]
    try:
        os.mkdir(dirname)
    except:
        pass
        
    #outputFile = "output.raw"
    outputname = dirname  + "_" + str(QF)
    outputFile = "./"+ dirname + "/" + outputname + ".simplejpeg"
    recoverFile = "./"+ dirname + "/" + outputname + "_recover.raw"
    
    if mode is "c":
        with open(inputFile, "rb") as input_:
            with contextlib.closing(BitWriter(open(outputFile, "wb"))) as bitout:
                encoder = Encoder(input_, bitout)
                encoder.setQF(QF)
                encoder.setBpp(int(bpp))
                encoder.compress()
    elif mode is "d":    
        with contextlib.closing(BitReader(open(outputFile, "rb"))) as input_:
            with open(recoverFile, "wb") as bitout:
                decoder = Decoder(input_, bitout)
                decoder.setQF(QF)
                decoder.setBpp(int(bpp))
                decoder.decompress()
    elif mode is "p":
        with open(inputFile,'rb') as f_1:
            with open(recoverFile,'rb') as f_2:
                image1 = f_1.read()
                image2 = f_2.read()
                image1 = np.reshape(list(image1),(512, 512, int(bpp)))
                image2 = np.reshape(list(image2),(512, 512, int(bpp)))
                mse = MSE(image1, image2, int(bpp))
                print("PSNR:",PSNR(mse))
    else:
        print(mode)
        raise Exception("Mode should be -c or -d")