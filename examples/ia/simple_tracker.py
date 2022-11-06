import pygame, sys
from pygame.locals import *
from math import sqrt, pow

class Circle():
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.vec = pygame.Vector2(0,0)
        self.memTimer = 60000
        
        
    def circle_collide(self, circle):
        if sqrt(pow(circle.x - self.x, 2) + pow(circle.y - self.y, 2)) < (circle.r + self.r):
            self.vec = pygame.Vector2(circle.x - self.x, circle.y - self.y).normalize()
            
            self.memTimer = 6000
            
    
    def track(self):
        if self.memTimer:
            self.x += + (self.vec * 0.05).x
            self.y += + (self.vec * 0.05).y
            self.memTimer -= 1
            pygame.draw.line(display, (0,255,0), (self.x, self.y), pygame.Vector2(self.x, self.y) + self.vec * 20)
        
circle1 = Circle(200, 130, 100)
circle2 = Circle(0, 0, 25)

pygame.init()

display = pygame.display.set_mode((800,600), DOUBLEBUF)

while 1:
    display.fill((30,20,30))
    
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
            
    mx, my = pygame.mouse.get_pos()
    
    circle2.x = mx
    circle2.y = my
    
    pygame.draw.circle(display, (160,60,60), (circle1.x, circle1.y), circle1.r, 1)
    pygame.draw.circle(display, (160,60,60), (circle1.x, circle1.y), 3)
    pygame.draw.circle(display, (160,60,60), (circle2.x, circle2.y), circle2.r, 1)
    pygame.draw.circle(display, (160,60,60), (circle2.x, circle2.y), 3)
    
    circle1.circle_collide(circle2)
    circle1.track()

    pygame.display.flip()