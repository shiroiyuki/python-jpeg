# coding=utf8
"""
bit I/O

Student ID: 107522049
Author: Cheng-Hsin Wang
Country: ROC
School: NCU 
"""
class BitStream(object):
    def __init__(self):
        self.currentbyte = 0
        self.bitscount = 0
            
class BitReader(BitStream):
    def __init__(self, input):
        super().__init__()
        self.input = input  # The underlying byte stream to write to
    
    def readbit(self):
        if self.currentbyte == -1:
            return -1
        if self.bitscount == 0:
            temp = self.input.read(1)
            if len(temp) == 0:
                self.currentbyte = -1
                return -1
            self.currentbyte = temp[0]
            self.bitscount = 8
        self.bitscount -= 1
        return (self.currentbyte >> self.bitscount) & 1
        
    def read_no_eof(self):
        result = self.readbit()
        if result != -1:
            return result
        else:
            raise EOFError()
            
    def close(self):
        self.input.close()

        
class BitWriter(BitStream):
    
    # Constructs a bit output stream based on the given byte output stream.
    def __init__(self, output):
        super().__init__()
        self.output = output  

    # Writes a bit to the stream. The given bit must be 0 or 1.
    def writebit(self, b):
        if b not in (0, 1):
            raise ValueError("Argument must be 0 or 1")
        self.currentbyte = (self.currentbyte << 1) | b
        self.bitscount += 1
        if self.bitscount == 8:
            self.output.write(bytes([self.currentbyte]))
            self.currentbyte = 0
            self.bitscount = 0

    # Closes this stream and the underlying output stream. If called when this
    # bit stream is not at a byte boundary, then the minimum number of "0" bits
    # (between 0 and 7 of them) are written as padding to reach the next byte boundary.
    def close(self):
        while self.bitscount != 0:
            self.writebit(0)
        self.output.close()