import pygame
import random
from enum import Enum
from collections import namedtuple, deque
from itertools import islice

pygame.init()

font = pygame.font.SysFont('arial', 25)

Point = namedtuple('Point', 'x, y')

RIGHT = Point( 1, 0)
LEFT  = Point(-1, 0)
UP    = Point( 0,-1)
DOWN  = Point( 0, 1)

BLOCK_SIZE = 20
FPS = 10

WHITE = (255,255,255)
RED   = (200,  0,  0)
BLUE1 = (0  ,  0,255)
BLUE2 = (0  ,100,255)
BLACK = (0  ,  0,  0)

class Game:
    def __init__(self, w=640, h=480):
        #screen attributes
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()

        #snake attributes
        self.direction = RIGHT
        self.body = deque([
            Point(self.w/2, self.h/2),
            Point(self.w/2-BLOCK_SIZE, self.h/2),
            Point(self.w/2-(2*BLOCK_SIZE), self.h/2),
        ])
        self.head = self.body[0]
        
        #game attributes
        self.score = 0
        self.food = Point(0,0)
        self._place_food()
    
    def play(self):
        
        #user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                #check if user input is not opposite to current direction and assign
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if not self.direction == RIGHT:
                        self.direction = LEFT
                elif event.key == pygame.K_RIGHT:
                    if not self.direction == LEFT:
                        self.direction = RIGHT
                elif event.key == pygame.K_UP:
                    if not self.direction == DOWN:
                        self.direction = UP
                elif event.key == pygame.K_DOWN:
                    if not self.direction == UP:
                        self.direction = DOWN
                    
        #move snake
        self.body.appendleft(Point(
            self.head.x + self.direction.x * BLOCK_SIZE,
            self.head.y + self.direction.y * BLOCK_SIZE
            ))
        self.body.pop()
        self.head = self.body[0]
        
        #check collision
        game_state = True
        if self._check_collision():
            return False, self.score
        
        #check food
        if self._check_food():
            #add food to body
            self.body.appendleft(Point(
            self.food.x,
            self.food.y
            ))
            self.head = self.body[0]
            
            #add food to area
            self._place_food()
            
        #update score
        self.score = len(self.body)-3
        
        #update ui
        self._update_ui()
        self.clock.tick(FPS)
        
        #return game status and score
        return game_state, self.score
    
    def _place_food(self):
        if self.food is not None:
            self.food = Point(
                random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE,
                random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
                )
            if self.food in self.body:
                self._place_food()
    
    def _check_collision(self):
        #check if head touches edge of screen
        condition1 = ((self.head.x > (self.w-BLOCK_SIZE))  
                        or (self.head.x < 0) 
                        or (self.head.y > (self.h-BLOCK_SIZE))  
                        or (self.head.y < 0))
        
        #check if edge touches body
        condition2 = (self.head in islice(self.body,1,len(self.body)))
        return condition1 or condition2
    
    def _check_food(self):
        return (self.head == self.food)
    
    def _update_ui(self):
        self.display.fill(BLACK)
        
        for point in self.body:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(point.x, point.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(point.x+4, point.y+4, BLOCK_SIZE-8, BLOCK_SIZE-8))
        
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
            
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

if __name__ == '__main__':
    game = Game()
    while True:
        game_state, score = game.play()

        if game_state == False:
            break
        