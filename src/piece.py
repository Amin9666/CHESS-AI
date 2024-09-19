import os

class Piece:
    
    def __init__(self, name, color, value, texture=None, texture_rect=None):
        self.name = name
        self.color = color 
        value_sign = 1 if color == 'white' else -1
        self.value = value * value_sign
        self.moves = []
        self.moved = False
        self.texture = texture
        self.set_texture()
        self.texture_rect = texture_rect
        
    def set_texture(self, size=80):
        self.texture = os.path.join(
            f'assets/images/imgs-{size}px/{self.color}_{self.name}.png'
        )
        
    def add_moves(self, move):
        self.moves.append(move)
        
    def clear_moves(self):
        self.moves = []

    # Add a method to check if the piece is white or black
    def is_white(self):
        return self.color == 'white'
    
    def is_black(self):
        return self.color == 'black'

    # Define a placeholder for the symbol() method to be implemented in subclasses
    def symbol(self):
        raise NotImplementedError("This method should be implemented by subclasses")

    
class Pawn(Piece):
    
    def __init__(self, color):
        self.dir = -1 if color == 'white' else 1
        super().__init__('pawn', color, 1.0)

    def symbol(self):
        return 'P' if self.is_white() else 'p'
        
class Knight(Piece):

    def __init__(self, color):
        super().__init__('knight', color, 3.0)

    def symbol(self):
        return 'N' if self.is_white() else 'n'
        
class Bishop(Piece):
    
    def __init__(self, color):
        super().__init__('bishop', color, 3.001)

    def symbol(self):
        return 'B' if self.is_white() else 'b'
        
class Rook(Piece):

    def __init__(self, color):
        super().__init__('rook', color, 5.0)

    def symbol(self):
        return 'R' if self.is_white() else 'r'
        
class Queen(Piece):
    
    def __init__(self, color):
        super().__init__('queen', color, 9.0)

    def symbol(self):
        return 'Q' if self.is_white() else 'q'
        
class King(Piece):
    
    def __init__(self, color):
        super().__init__('king', color, 1000000.0)

    def symbol(self):
        return 'K' if self.is_white() else 'k'