# coding=utf8
"""
define HuffmanTree structure
 
Student ID: 107522049
Author: Cheng-Hsin Wang
Country: ROC
School: NCU 
"""
class Node(object):
    pass

# An internal node in a code tree. It has two nodes as children.
class InternalNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right


# A leaf node in a code tree. It has a symbol value.
class Leaf(Node):
    def __init__(self, run, size):
        # set default value is error or nonsense
        self.run = run 
        self.size = size

class HuffmanTree(object):
    def __init__(self):
        self.Tree = InternalNode(None, None)
    
    def buildTree(self, code):
        def _buildTree(symbol, run=-1, size=-1):
            self.tmp = self.Tree
            for i in symbol[:-1]:
                if i is "1":
                    if self.tmp.right is None:
                        self.tmp.right = InternalNode(None,None)
                    self.tmp = self.tmp.right
                else:
                    if self.tmp.left is None:
                        self.tmp.left = InternalNode(None,None)
                    self.tmp = self.tmp.left
            if symbol[-1] is "1":
                if not self.tmp.right is None:
                    print(symbol,run,size)
                    raise Exception("Wrong right")
                self.tmp.right = Leaf(run, size)
            else:
                if not self.tmp.left is None:
                    print(symbol,run,size)
                    raise Exception("Wrong left")
                self.tmp.left = Leaf(run, size)
                
        
        listFlag = isinstance(code[0],list)
        
        if listFlag: # AC Hcode
            for i in code:
                index_x = code.index(i)
                for j in i:
                    if j is None:
                        continue
                    #print(index_x, i.index(j), j)
                    _buildTree(j, index_x, i.index(j))
        else: # DC HCode
            for i in code: 
                _buildTree(i, size = code.index(i))
    
    def readSymbol(self, symbol):
        self.tmp = self.Tree
        for i in symbol[:-1]:
            if i is "1":
                self.tmp = self.tmp.right
            else:
                self.tmp = self.tmp.left
        self.tmp = self.tmp.right if symbol[-1] is "1" else self.tmp.left
        return self.tmp.run,self.tmp.size