class Move:
    
    def __init__(self, initial, final):
        self.initial = initial
        self.final = final

    def __str__(self):
        s = ''
        s += f'({self.initial.col}, {self.initial.row})'
        s += f' -> ({self.final.col}, {self.final.row})'
        return s

    def __eq__(self, other):
        return self.initial == other.initial and self.final == other.final

    def to_uci(self):
        """Converts the move to UCI (algebraic) notation."""
        return self.square_to_uci(self.initial) + self.square_to_uci(self.final)

    def square_to_uci(self, square):
        """Converts a square (row, col) to UCI notation."""
        files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']  # File letters for columns
        return files[square.col] + str(8 - square.row)  # Rows are inverted in UCI