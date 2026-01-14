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
    isCheck = False
    pinned = False
    isValid = True

    def __init__(self, x, y, tgtX, tgtY, isCheck=False, pinned=False, isValid=True):
        self.x = x
        self.y = y
        self.tgtX = tgtX
        self.tgtY = tgtY
        self.isCheck = isCheck
        self.pinned = pinned
        self.isValid = isValid

    def unpack(self):
        return self.x,self.y,self.tgtX,self.tgtY

    def unpack_full(self):
        return self.x,self.y,self.tgtX,self.tgtY,self.isCheck,self.pinned
    
    def __str__(self):
        return f"x : {self.x}, y : {self.y}, tgtX : {self.tgtX}, tgtY : {self.tgtY}, isCheck = {self.check}, isPin = {self.pinned}"
    
class evalObj:
    eval = 0
    move = ''

    def __init__(self, eval, moveStats):
        self.eval = eval
        self.move = moveStats