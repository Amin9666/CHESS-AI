class Piece:
    
    def __init__(self, name, color, value, texture, teture_rect=None):
        pass
    
class Pawn(Piece):
    
    def __init__(self, color):
        self.dir = -1 if color == 'white' else 1
        if color == 'white':
            self.dir = -1
        else:
            self.dir = 1