import pygame
import sys

from const import *
from game  import Game

class Main:
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')
        self.game = Game()

    def mainloop(self):
        
        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger
        
        
        while True:
            game.show_bg(screen)
            game.show_pieces(screen)
            
            for event in pygame.event.get():
                
                #click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.mouseY // SQSIZE 
                    clicked_col = dragger.mouseX // SQSIZE 
                    
                    
                    if board.squares[clicked_row][clicked_col].has_piece():
                        pass

                    
                #mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    pass
                
                #clik release
                elif event.type == pygame.MOUSEBUTTONUP:
                    pass
                
                #quit 
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            
            
                       
            pygame.display.update()    
    
main = Main()
main.mainloop()