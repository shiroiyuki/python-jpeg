# coding=utf8
""" 
some widgets

Author: Cheng-Hsin Wang
Country: ROC 
"""
import numpy as np
import math
def zigzag_points(rows, cols):
    # constants for directions
    UP, DOWN, RIGHT, LEFT, UP_RIGHT, DOWN_LEFT = range(6)

    # move the point in different directions
    def move(direction, point):
        return {
            UP: lambda point: (point[0] - 1, point[1]),
            DOWN: lambda point: (point[0] + 1, point[1]),
            LEFT: lambda point: (point[0], point[1] - 1),
            RIGHT: lambda point: (point[0], point[1] + 1),
            UP_RIGHT: lambda point: move(UP, move(RIGHT, point)),
            DOWN_LEFT: lambda point: move(DOWN, move(LEFT, point))
        }[direction](point)

    # return true if point is inside the block bounds
    def inbounds(point):
        return 0 <= point[0] < rows and 0 <= point[1] < cols

    # start in the top-left cell
    point = (0, 0)

    # True when moving up-right, False when moving down-left
    move_up = True

    for i in range(rows * cols):
        yield point
        if move_up:
            if inbounds(move(UP_RIGHT, point)):
                point = move(UP_RIGHT, point)
            else:
                move_up = False
                if inbounds(move(RIGHT, point)):
                    point = move(RIGHT, point)
                else:
                    point = move(DOWN, point)
        else:
            if inbounds(move(DOWN_LEFT, point)):
                point = move(DOWN_LEFT, point)
            else:
                move_up = True
                if inbounds(move(DOWN, point)):
                    point = move(DOWN, point)
                else:
                    point = move(RIGHT, point)
    
def dpcm(src, pred):
    diff = (src - pred) //2
    pred = pred + diff * 2   # rebuild
    return diff, pred

def idpcm(diff, pred):
    rev = (diff * 2 + pred) 
    return rev, rev

'''
def ycbcr2rgb(block):
    rgb = np.empty((8, 8, 3), dtype=np.uint8)
    for i in range(8):
        for j in range(8):
            rgb[i][j][0] = block[i][j][0] + 1.402*(block[i][j][2]-128)
            rgb[i][j][1] = block[i][j][0] - 0.34414*(block[i][j][1]-128)- 0.71414*(block[i][j][2]-128)
            rgb[i][j][2] = block[i][j][0] + 1.772*(block[i][j][1]-128)
    return (rgb)

def rgb2ycbcr(block):
    ycbcr = np.empty((8, 8, 3), dtype=np.float)
    for i in range(8):
        for j in range(8):
            ycbcr[i][j][0] = 0.299*(block[i][j][0] - block[i][j][1]) + block[i][j][1] + 0.114*(block[i][j][2] - block[i][j][1])
            ycbcr[i][j][1] = 0.5643*(block[i][j][2] - ycbcr[i][j][0])
            ycbcr[i][j][2] = 0.7133*(block[i][j][0] - ycbcr[i][j][0])
                
    return (ycbcr)
'''

def rgb2ycbcr(im):
    xform = np.array([[.299, .587, .114], [-.1687, -.3313, .5], [.5, -.4187, -.0813]])
    ycbcr = im.dot(xform.T)
    ycbcr[:,:,[1,2]] += 128
    return np.uint8(ycbcr)

def ycbcr2rgb(im):
    xform = np.array([[1, 0, 1.402], [1, -0.34414, -.71414], [1, 1.772, 0]])
    rgb = im.astype(np.float)
    rgb[:,:,[1,2]] -= 128
    rgb = rgb.dot(xform.T)
    np.putmask(rgb, rgb > 255, 255)
    np.putmask(rgb, rgb < 0, 0)
    return np.uint8(rgb)
    
def binstrFlip(binstr):
    return ''.join(map(lambda c: '0' if c == '1' else '1', binstr))

def int2binstr(n):
    return bin(abs(n))[2:] if n > 0 else binstrFlip(bin(abs(n))[2:])

# category for ac or dc 
def categorize(n):
    n = abs(n)
    result = 0
    while n > 0:
        n >>= 1
        result += 1
    return result
    