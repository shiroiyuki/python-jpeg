# coding=utf8
""" 
Author: Cheng-Hsin Wang
Country: ROC 
"""
# jpeg codec
# encoding process:
#   read raw data
#   spilt data to 8*8 block
#   convert RGB into Ybcbr
#   sub_sampling
#   level_offset
#   2d_DCT
#   Quantization
#   Zigzag process
#   DC differential Coding
#   AC Run-Length Coding (RLC)
#   Coefficient Coding Categories
#   write to bitstream

    
# decoding process:
#   read bitstream
#   decode with Coefficient Coding (huffman code + fixed code)
#   get zigzag data
#   recover to 8*8 block
#   Dequantization
#   2d_iDCT  
#   level_offset
#   convert Ybcbr into RGB
#   write to bitstream    
   
    
# Reference: 
# http://chu246.blogspot.com/2013/11/huffman-coding-for-dc-ac-coefficients.html
# https://www.cnblogs.com/buaaxhzh/p/9119870.html
# https://hk.saowen.com/a/eab40bbcd7a356d06bd3d9644d611a623f628dec8da75a6e70ff65750f7a2334
# https://github.com/ghallak/jpeg-python