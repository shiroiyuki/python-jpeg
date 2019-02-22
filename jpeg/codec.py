# coding=utf8
""" 
simple jpeg codec

Student ID: 107522049
Author: Cheng-Hsin Wang
Country: ROC
School: NCU 
"""
from . import codeBook
from .quantizationTable import Luminance, Chrominance
from .huffman import HuffmanTree, Leaf, InternalNode
from .utils import *
from .bitio import BitWriter, BitReader

from scipy import fftpack
import numpy as np
import math

class codec(object):

    def __init__(self):
        self.bpp = 1 #byte per pixel
        self.qualityFactor = 50
        self.blockcount = 0
        self.setQF(self.qualityFactor)
        
    def setQF(self,qualityFactor):
        if qualityFactor <= 0 or qualityFactor >=100:
            raise ValueError("QualityFactor must be in (0,100)")
        elif qualityFactor >=50:
            self.factor = 200-2*qualityFactor
        else:
            self.factor = 5000/qualityFactor
        self.loadQB()
        
    def loadQB(self):
        self.Luminance = Luminance(self.factor)
        self.Chrominance = Chrominance(self.factor)
    
    def setBpp(self, bpp=1):
        self.bpp = bpp
        self.blockcount *= self.bpp
        
class Encoder(codec):

    def __init__(self, reader=None, writer=None):
        super().__init__()
        self.reader = reader
        self.writer = writer
        self.codeDict = {"DCLUM" : codeBook.DCLUMCODE,
                        "DCCHROM": codeBook.DCCHROMCODE,
                        "ACLUM": codeBook.ACLUMCODE,
                        "ACCHROM": codeBook.ACCHROMCODE
        }
            
    def compress(self):
        rawData = self.reader.read()
        graylevel = True
        
        if len(rawData) > 512*512:
            rawData = np.reshape(list(rawData),(512, 512, 3))
            self.setBpp(3)
            graylevel = False
        else:
            rawData = np.reshape(list(rawData),(512, 512, 1))
        
        print("BPP: ",self.bpp)

        rows, cols, _ = rawData.shape
        blocks_count = rows // 8 * cols // 8
        
        first = [0, 0, 0]
        
        pred = first.copy()
        for i in range(0, rows, 8):
            for j in range(0, cols, 8):
                tblock = (rawData[i:i+8, j:j+8]).astype(np.float)
                if not graylevel:
                    tblock = rgb2ycbcr(tblock)
                    tblock = self.subsampling(tblock)
                    
                    
                for k in range(self.bpp):

                    block = tblock[:, :, k]
                    block = self.levelOffset(block)
                    dct_matrix = self.dct_2d(block)
                    quant_matrix = self.quantize(dct_matrix,
                                            self.Luminance if k == 0 else self.Chrominance)
                    zz = self.block2zigzag(quant_matrix)
                    diff, pred[k] = dpcm(zz[0], pred[k])
                    #diff = zz[0]
                    
                    if j == 0:
                        first[k] = pred[k]
                        
                    self.writeDC(diff,"DCLUM" if k == 0 else "DCCHROM")
                    self.writeAC(self.run_length_encode(zz[1:]), "ACLUM" if k == 0 else "ACCHROM")
            
            pred = first.copy()

            
    def writeDC(self, num, DCtable):
        #print(DCtable)
        bincode = self._getbinCode(num)
        #if self.codeDict[DCtable][categorize(num)] is "00":
            #print("00 bincode: ",bincode)
        try:
            self._writeSymbol(self.codeDict[DCtable][categorize(num)])
        except:
            print(categorize(num))
            raise ValueError("Wrong")
        if bincode:
            self._writeSymbol(bincode)
    
    def writeAC(self, RLE, ACtable):
        #print(ACtable)
        #if self.codeDict[ACtable][categorize(num)] is "00":
            #print("00 bincode: ",bincode)
        
        for RS, bincode in zip(*RLE):
            try:
                self._writeSymbol(self.codeDict[ACtable][RS[0]][RS[1]])
            except:
                print(RS)
                raise ValueError("Wrong")
            if bincode:
                self._writeSymbol(bincode)

    
    def _writeSymbol(self,symbol):
        #print(symbol)
        for i in symbol:
            self.writer.writebit(int(i))
    
    def _getbinCode(self, num):
        return int2binstr(int(num)) if not num == 0 else None
        
    @classmethod    
    def subsampling(cls,block):
        for i in range(0,8,2):
            for j in range(0,8,2):
                cb = block[i][j][1] #+ block[i+1][j][1] + block[i][j+1][1] + block[i+1][j+1][1])/4 
                cr = block[i][j][2] #+ block[i+1][j][2] + block[i][j+1][2] + block[i+1][j+1][2])/4
                block[i][j][1] = block[i+1][j][1] = block[i][j+1][1] = block[i+1][j+1][1] = cb
                block[i][j][2] = block[i+1][j][2] = block[i][j+1][2] = block[i+1][j+1][2] = cr
        return block
            
    @classmethod
    def quantize(cls, block, qTable):
        return (block / qTable).round().astype(np.int32)        
    
    @classmethod
    def dct_2d(cls, block):
        return fftpack.dct(fftpack.dct(block.T, norm='ortho').T, norm='ortho')

    @classmethod
    def levelOffset(cls, data):
        return data - 128
    
    @classmethod
    def block2zigzag(cls, block):
        return np.array([block[point] for point in zigzag_points(*block.shape)])
           
    def run_length_encode(self, arr):
        # determine where the sequence is ending prematurely
        last_nonzero = -1
        for i, elem in enumerate(arr):
            if elem != 0:
                last_nonzero = i

        # each symbol is a (RUNLENGTH, SIZE) tuple
        symbols = []

        # values are binary representations of array elements using SIZE bits
        values = []

        run_length = 0
        for i, elem in enumerate(arr):
            if i > last_nonzero:
                symbols.append((0, 0)) #EOB
                values.append(None)
                break
            elif elem == 0 and run_length < 15:
                run_length += 1
            else:
                size = categorize(elem)
                symbols.append((run_length, size))
                values.append(self._getbinCode(elem))
                run_length = 0
        return symbols, values  

class Decoder(codec):

    def __init__(self, reader=None, writer=None):
        super().__init__()
        self.reader = reader
        self.writer = writer
        self.initTree()
        self.treeDict = {"DCLUM" : self.H_DC_LUM,
                        "DCCHROM": self.H_DC_CHROM,
                        "ACLUM"  : self.H_AC_LUM,
                        "ACCHROM": self.H_AC_CHROM
        }
        
    def initTree(self):
        #print("ACLUM")
        self.H_AC_LUM = HuffmanTree()
        self.H_AC_LUM.buildTree(codeBook.ACLUMCODE)
        #print("ACCHROM")
        self.H_AC_CHROM = HuffmanTree()
        self.H_AC_CHROM.buildTree(codeBook.ACCHROMCODE)
        #print("DCLUM")
        self.H_DC_LUM = HuffmanTree()
        self.H_DC_LUM.buildTree(codeBook.DCLUMCODE)
        #print("DCCHROM")
        self.H_DC_CHROM = HuffmanTree()
        self.H_DC_CHROM.buildTree(codeBook.DCCHROMCODE)
    
    def decompress(self):
        
        blockcounts = 4096 
        currentBlock = 0
        blocks_per_line = 64
        blockSide = 8

        pred = first = 0
        buffer = np.empty((512, 512, self.bpp), dtype=np.float)
        i = j = 0
        graylevel = False
        if self.bpp == 1:
            graylevel = True
        first = [0, 0, 0]
        sideblock = 0
        count = 0
        pred = first.copy()
        while True:
            i = currentBlock // blocks_per_line * blockSide
            j = currentBlock % blocks_per_line * blockSide
            for k in range(self.bpp):
                zz = []

                run, size = self.read("DCLUM" if k == 0 else "DCCHROM")

                number = self.decode(size)

                acblock = 63
    
                number, pred[k] = idpcm(number ,pred[k])
                if sideblock == 0:
                    first[k] = pred[k]
                zz.append(number)
                    
                while True:
                    run, size = self.read("ACLUM" if k == 0 else "ACCHROM")
                    
                    if self.is_EOB(run, size):
                        temp = [0 for i in range(acblock)]
                        zz += temp
                        break

                    acblock -= (run + 1)
                    zz += self.decodeRLE(run, size)
                    if acblock == 0:
                        break
                
                
                
                quant_matrix = self.zigzag_to_block(zz)
                dct_matrix = self.dequantize(quant_matrix,
                                            self.Luminance if k == 0 else self.Chrominance)
                block = self.idct_2d(dct_matrix)
                block = self.ilevelOffset(block)
                buffer[i:i+8, j:j+8, k] = block 
            
            if not graylevel:
                buffer[i:i+8, j:j+8] = ycbcr2rgb(buffer[i:i+8, j:j+8])
            buffer = buffer.astype(np.uint8)    

            
            
            
            currentBlock += 1
            sideblock += 1
            if sideblock == 64:
                sideblock = 0 
                pred = first.copy()
                
            if currentBlock == 4096:
                for i in range(512):
                    for j in range(512):
                        for k in range(self.bpp):
                            self.writer.write(bytes([(buffer[i,j,k])]))
                break


                
    
    def read(self, huffmanTree):
        currentnode = self.treeDict[huffmanTree].Tree
        while True:
            temp = self.reader.read_no_eof()
            if   temp == 0: nextnode = currentnode.left
            elif temp == 1: nextnode = currentnode.right
            else: raise AssertionError("Invalid value from read_no_eof()")
            
            if isinstance(nextnode, Leaf):
                return nextnode.run , nextnode.size
            elif isinstance(nextnode, InternalNode):
                currentnode = nextnode
            else:
                print(type(nextnode))
                raise AssertionError("Illegal node type")
    
    def is_EOB(self, run, size):
        return True if size == 0 and run == 0 else False
    
    def fillEOB(self):
        return
        
    def decodeRLE(self, run, size):
        temp = []
        while run:
            temp.append(0)
            run -=1
        temp.append(self.decode(size))
        return temp
        
    def decode(self, size):
        number = 0
        Firstbit = True
        signbit = False
        while size:
            temp = self.reader.readbit()
            #print(temp)
            if Firstbit:
                Firstbit = False
                if not (temp & 1):
                    signbit = True
            number = (number << 1)| (temp ^ 1) if signbit else (number << 1)| temp
            size -= 1
        return -number if signbit else number
        
    @classmethod
    def dequantize(cls, block, qTable):
        return block * qTable        
    
    @classmethod
    def idct_2d(cls, block):
        return fftpack.idct(fftpack.idct(block.T, norm='ortho').T, norm='ortho')

    @classmethod
    def ilevelOffset(cls, data):
        return data + 128
    
    @classmethod
    def zigzag_to_block(cls, zigzag):
        # assuming that the width and the height of the block are equal
        rows = cols = int(math.sqrt(len(zigzag)))
        #print(len(zigzag))
        if rows * cols != len(zigzag):
            print("zz len:",len(zigzag))
            raise ValueError("length of zigzag should be a perfect square")

        block = np.empty((rows, cols), np.int32)

        for i, point in enumerate(zigzag_points(rows, cols)):
            block[point] = zigzag[i]

        return block

               