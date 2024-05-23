import pygame
import sys

from const import *
from game  import Game
from square import Square
from move import Move

class Main:
    
    def __init__(self):
        pygame.init()
        #self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption('Chess')
        self.game = Game()
        

    def mainloop(self):
        
        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger
        
        
        while True:
            game.show_bg(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            
            if dragger.dragging:
                dragger.update_blit(screen)
            
            for event in pygame.event.get():
                
                #click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.mouseY // SQSIZE 
                    clicked_col = dragger.mouseX // SQSIZE 

                    #if clicked square has a piece
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        # valid piece color ?
                        if piece.color == game.next_player:   
                            board.calc_moves(piece, clicked_row, clicked_col)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)

                            game.show_bg(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)

                    
                #mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        game.show_bg(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        dragger.update_blit(screen)
                
                #clik release
                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        
                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE
                        
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)
                        
                        if board.valid_move(dragger.piece, move):
                            board.move(dragger.piece, move)
                            
                            #methods
                            game.show_bg(screen)
                            game.show_pieces(screen)
                            
                            #next turn
                            game.next_turn()
                            
                            
                    dragger.undrag_piece()
                    
                    
                
                #quit 
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            
            
                       
            pygame.display.update()    
    
main = Main()
main.mainloop()

