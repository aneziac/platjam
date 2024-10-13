import pygame as pg
import platjam.colors as colors

class Player:
    pg.init()

    
    def __init__ (self, screen):
        self.screen = screen
        self.screen.WIDTH= self.screen.WIDTH+20

        
        self.player_pos = pg.Vector2(self.screen.WIDTH//2, self.screen.HEIGHT//2)
        self.player_velocity = 0
        print (self.screen.HEIGHT)
      #  pg.draw.circle(screen._canvas, "red", self.player_pos, 40)
      
    def update(self, keys, grounded):
        
        if self.player_pos.y>=(self.screen.HEIGHT-25):   
            grounded=True
                
        if not grounded:
            self.player_velocity -= 5*
            self.player_pos.y += self.player_velocity
        
        if (keys[pg.K_w] or keys[pg.K_UP]) and grounded:  
#            self.player_pos.y -= 20
            self.player_velocity = 20
            
            grounded = False
    
#        if keys[pg.K_s] or keys[pg.K_DOWN]:
#           if self.player_pos.y<(self.screen.HEIGHT-25):   
#                self.player_pos.y += 5
#                grounded=True
                
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            if self.player_pos.x>0:   
                self.player_pos.x -= 5
            else:
                self.player_pos.x= self.screen.WIDTH
                
        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            if self.player_pos.x<self.screen.WIDTH:   
                self.player_pos.x += 5   
            else:
                self.player_pos.x=0
                   
    def render(self):
        self.screen.circle(self.player_pos, 20, colors.PURPLE)
            
            
        
        
        