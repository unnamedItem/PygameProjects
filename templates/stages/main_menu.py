import pygame, sys
from pygame.locals import *

import commons
from constants import *
from stages.stage import Stage
import stages.index as stages


class MainMenu(Stage):
    def __init__(self):
        self.font_title:pygame.font.Font = pygame.font.Font(None, 80)
        self.font_options:pygame.font.Font = pygame.font.Font(None, 40)
        self.title:list = [self.font_title.render("MENU", True, WHITE), (60,60), pygame.rect.Rect(0,0,0,0)]
        self.options:list = [
            ["Start", WHITE, (60, 400), pygame.rect.Rect(0,0,0,0)],
            ["Exit Game", WHITE, (60, 440), pygame.rect.Rect(0,0,0,0)],
        ]


    def events(self, event:pygame.event.Event) -> None:
        if event.type == MOUSEBUTTONDOWN:
            if commons.mouse_pressed[0]:
                for index, option in enumerate(self.options):
                    if pygame.rect.Rect.collidepoint(option[3], commons.mouse_pos):
                        if index == 0:
                            stages.active_stage = stages.stage_testing
                        if index == 1:
                            sys.exit()
        
        if event.type == MOUSEMOTION:
            for index, option in enumerate(self.options):
                if pygame.rect.Rect.collidepoint(option[3], commons.mouse_pos):
                    option[1] = GREEN
                else:
                    option[1] = WHITE


    def render(self, display: pygame.surface.Surface) -> None:
        self.title[2] = display.blit(self.title[0], self.title[1])
        for option in self.options:
            option[3] = display.blit(self.font_options.render(option[0], True, option[1]), option[2])