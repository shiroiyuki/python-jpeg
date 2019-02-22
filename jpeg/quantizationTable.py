# coding=utf8
"""
default quantization table for Luminance and Chrominance

Author: Cheng-Hsin Wang
Country: ROC 
"""
import numpy as np

class QuantizationTable(object):
    def __init():
        pass
        
    def __str__(self):
        return str(self.table)
    
    def __iter__(self):
        for i in self.table:
            yield i
        
    def __getitem__(self, i):
        return self.table[i]
        
    def __len__(self):
        return len(self.table)

class Luminance(QuantizationTable):
    def __init__(self, quality = 100):
        super().__init__()
        self.table = np.array([[16, 11, 10, 16, 24, 40, 51, 61],
                      [12, 12, 14, 19, 26, 58, 60, 55],
                      [14, 13, 16, 24, 40, 57, 69, 56],
                      [14, 17, 22, 29, 51, 87, 80, 62],
                      [18, 22, 37, 56, 68, 109, 103, 77],
                      [24, 36, 55, 64, 81, 104, 113, 92],
                      [49, 64, 78, 87, 103, 121, 120, 101],
                      [72, 92, 95, 98, 102, 100, 103, 99]])
        self.table = (self.table * quality/100).round().astype(np.int32)
        
class Chrominance(QuantizationTable):
    def __init__(self, quality = 100):
        super().__init__()
        self.table = np.array([[17, 18, 24, 47, 99, 99, 99, 99],
                      [18, 21, 26, 66, 99, 99, 99, 99],
                      [24, 26, 56, 99, 99, 99, 99, 99],
                      [47, 66, 99, 99, 99, 99, 99, 99],
                      [99, 99, 99, 99, 99, 99, 99, 99],
                      [99, 99, 99, 99, 99, 99, 99, 99],
                      [99, 99, 99, 99, 99, 99, 99, 99],
                      [99, 99, 99, 99, 99, 99, 99, 99]])
        self.table = (self.table * quality/100).round().astype(np.int32)