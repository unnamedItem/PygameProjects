import os
import pygame, sys, time
from pygame.locals import *

import commons
from constants import *

pygame.init()

import stages.index as stages


class Game:
    def __init__(self) -> None:
        self.isRunning:bool = True

        self.display:pygame.Surface = pygame.display.set_mode(commons.display_size, DOUBLEBUF)

        self.main_clock:pygame.time.Clock = pygame.time.Clock()
        self.last_time:float = time.time()
        self.fps_max:float = 140.0
        self.fps:float = self.main_clock.get_fps()


    def run(self) -> None:
        while self.isRunning:       
            self.events()
            self.update()
            self.render()


    def events(self) -> None:
        for event in pygame.event.get():            
            if event.type == QUIT:
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                commons.mouse_pressed = pygame.mouse.get_pressed()

            if event.type == MOUSEBUTTONUP:
                commons.mouse_pressed = pygame.mouse.get_pressed()

            if event.type == MOUSEMOTION:
                commons.mouse_pos = pygame.mouse.get_pos()
                
            stages.active_stage.events(event)


    def update(self) -> None:
        commons.dt = self.delta_time()
        stages.active_stage.update()


    def render(self) -> None:
        self.display.fill(BACKGROUND_COLOR)
        stages.active_stage.render(self.display)
        self.fps_render()
        pygame.display.flip()

    
    def delta_time(self) -> float:
        self.main_clock.tick(self.fps_max)
        self.fps = self.main_clock.get_fps()
        dt = time.time() - self.last_time
        self.last_time = time.time()
        return dt
    
    def fps_render(self):
        fps:pygame.surface.Surface = pygame.font.Font(None, 40).render(str(int(self.fps)), True, WHITE)
        self.display.blit(fps, (commons.display_w - fps.get_size()[0] - 20, 20))
        


Game().run()