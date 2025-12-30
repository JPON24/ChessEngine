class positional_data:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

class square:
    position = ''
    typeOfPiece = ''
    color = ''

    def __init__(self, x, y, typeOfPiece, color):
        self.position = positional_data(x,y)
        self.typeOfPiece = typeOfPiece
        self.color = color

class Move:
    x = 0
    y = 0
    tgtX = 0
    tgtY = 0

    def __init__(self, x, y, tgtX, tgtY):
        self.x = x
        self.y = y
        self.tgtX = tgtX
        self.tgtY = tgtY

    def unpack(self):
        return self.x,self.y,self.tgtX,self.tgtY
    
class evalObj:
    eval = 0
    move = ''

    def __init__(self, eval, moveStats):
        self.eval = eval
        self.move = moveStats