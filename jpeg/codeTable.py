class CodeTable(object):
    pass

    
    
# DC codeword = Category codeword + DIFF value codeword
class DCLumCode(CodeTable):
    def __init__(self):
        self.codeWord = ['00','010','011','100','101','110',
                        '1110','11110','111110','1111110',
                        '11111110','111111110'
        ]

class DCChromCode(CodeTable):
    def __init__(self):
        self.codeWord = ['00','01','10','110','1110','11110',
                        '111110','1111110','11111110','111111110',
                        '1111111110','11111111110'
        ]
        
class ACLumCode(CodeTable):
    def __init__(self):
        self.codeWord = ['1010','00',