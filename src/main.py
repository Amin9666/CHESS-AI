import pygame
import sys
import chess
import chess.engine
from stockfish import Stockfish

from const import *
from game import Game
from square import Square
from move import Move

class Main:
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption('Chess')
        self.game = Game()

        # Initialize Stockfish engine
        self.stockfish = Stockfish(path="/opt/homebrew/bin/stockfish")
        self.stockfish.set_depth(15)  # You can set the search depth here
        self.stockfish.set_skill_level(10)  # You can adjust the skill level (0-20)

    def get_stockfish_move(self):
        """Get a move suggestion from Stockfish and apply it to the board."""
        board = self.game.board

        # Get FEN string from the board and set Stockfish's position
        fen = board.get_fen()  # Assuming your board has a method to get the FEN notation
        self.stockfish.set_fen_position(fen)

        # Get the best move from Stockfish
        best_move = self.stockfish.get_best_move()

        # Convert the move to your game's move format
        initial_square = best_move[:2]  # E.g., "e2"
        final_square = best_move[2:]  # E.g., "e4"

        initial_row, initial_col = self.game.get_square_indices(initial_square)
        final_row, final_col = self.game.get_square_indices(final_square)

        initial = Square(initial_row, initial_col)
        final = Square(final_row, final_col)

        move = Move(initial, final)

        # Apply the move
        piece = board.squares[initial_row][initial_col].piece
        board.move(piece, move)
        self.game.play_sound(False)  # No capture sound for simplicity

        # Update the display
        self.game.show_bg(self.screen)
        self.game.show_pieces(self.screen)
        pygame.display.update()

        # Move to the next turn
        self.game.next_turn()

    def mainloop(self):
        
        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger

        while True:
            # show methods
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            game.show_hover(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():

                # click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE

                    # if clicked square has a piece ?
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        # valid piece (color) ?
                        if piece.color == game.next_player:
                            board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)
                            # show methods 
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)
                
                # mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE

                    game.set_hover(motion_row, motion_col)

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        # show methods
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)
                
                # click release
                elif event.type == pygame.MOUSEBUTTONUP:
                    
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE

                        # create possible move
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)

                        # valid move ?
                        if board.valid_move(dragger.piece, move):
                            # normal capture
                            captured = board.squares[released_row][released_col].has_piece()
                            board.move(dragger.piece, move)

                            board.set_true_en_passant(dragger.piece)                            

                            # sounds
                            game.play_sound(captured)
                            # show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            # next turn
                            game.next_turn()

                            # Let Stockfish play if it's the next player's turn
                            if game.next_player == 'black':  # Assuming 'black' is Stockfish's color
                                self.get_stockfish_move()

                    dragger.undrag_piece()
                
                # key press
                elif event.type == pygame.KEYDOWN:
                    
                    # changing themes
                    if event.key == pygame.K_t:
                        game.change_theme()

                    # resetting game
                    if event.key == pygame.K_r:
                        game.reset()
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger

                    # toggle fullscreen/windowed mode
                    if event.key == pygame.K_f:
                        if self.screen.get_flags() & pygame.FULLSCREEN:
                            pygame.display.set_mode((WIDTH, HEIGHT))
                        else:
                            pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

                # quit application
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            pygame.display.update()

main = Main()
main.mainloop()