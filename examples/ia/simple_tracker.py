import pygame, sys, time
from pygame.locals import *
from math import sqrt, pow


pygame.init()

display = pygame.display.set_mode((800,600), DOUBLEBUF)
main_clock = pygame.time.Clock()
dt = 0.0
last_time = 0
overlap = None


class Circle():
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.vec = pygame.Vector2(0,0)
        self.memTimer = 2000
        
        
    def circle_collide(self, circle):
        if sqrt(pow(circle.x - self.x, 2) + pow(circle.y - self.y, 2)) < (circle.r + self.r):
            self.vec = pygame.Vector2(circle.x - self.x, circle.y - self.y).normalize()
            self.memTimer = 2000
            
    
    def track(self):
        if self.memTimer > 0:
            self.x += (self.vec * dt * 150).x
            self.y += (self.vec * dt * 150).y
            self.memTimer -= 1000 * dt
            pygame.draw.line(display, (0,255,0), (self.x, self.y), pygame.Vector2(self.x, self.y) + self.vec * 20)

CIRCLE1 = pygame.surface.Surface((200,200), SRCALPHA)
CIRCLE2 = pygame.surface.Surface((50,50), SRCALPHA)

circle1 = Circle(200, 130, 100)
circle2 = Circle(0, 0, 25)

pygame.draw.circle(CIRCLE1, (160,60,60), (100,100), circle1.r, 1)
pygame.draw.circle(CIRCLE1, (160,60,60), (100,100), 3)
pygame.draw.circle(CIRCLE2, (160,60,60), (25,25), circle2.r, 1)
pygame.draw.circle(CIRCLE2, (160,60,60), (25,25), 3)

BORDERS = pygame.surface.Surface((800,600), SRCALPHA)
borders_rect = pygame.draw.polygon(BORDERS, (255,255,255), [
    (0,0), (800,0), (800,600), (0,600), (20,580), (20, 20), (780, 20), (780, 580), (20,580), (0, 600)
])

border = BORDERS
border_mask = pygame.mask.from_surface(BORDERS)

POINTER = pygame.surface.Surface((1,1), SRCALPHA)
pointer_rect = pygame.draw.rect(POINTER, (255,255,255), (0,0,1,1))
pointer_mask = pygame.mask.from_surface(POINTER)
pointer = POINTER

while 1:
    main_clock.tick(140)
    dt = time.time() - last_time
    last_time = time.time()
    
    display.fill((30,20,30))
    
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()

    mx, my = pygame.mouse.get_pos()
    pointer_rect.x = mx
    pointer_rect.y = my
    
    circle1_rect = display.blit(CIRCLE1, (circle1.x-circle1.r, circle1.y-circle1.r))
    circle2_rect = display.blit(CIRCLE2, (circle2.x-circle2.r, circle2.y-circle2.r))
    
    offset = pointer_rect[0] - borders_rect[0], pointer_rect[1] - borders_rect[1]
    overlap = border_mask.overlap(pointer_mask, offset)
    if (not overlap):
        circle2.x = mx
        circle2.y = my
        

    circle1.circle_collide(circle2)
    circle1.track()
    
    display.blit(border, (0,0))
    display.blit(pointer, pointer_rect)

    pygame.display.flip()