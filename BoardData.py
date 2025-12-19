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