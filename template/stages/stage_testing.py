import pygame
from pygame.locals import *

from stages.stage import Stage
import stages.index as stages
from core.dialog_boxes import DialogBox

import commons
from constants import *

DEMO_TEXT = '\
    Welcome to simple dialog boxes!\n\
    This is a random text dialog.\n\
    \n\
    Goodbye!\
'


class StageTesting(Stage):
    def __init__(self):
        self.font_title:pygame.font.Font = pygame.font.Font(None, 60)
        self.title:list = [self.font_title.render("STAGE TESTING", True, WHITE), (60,60), pygame.rect.Rect(0,0,0,0)]
        
        self.dialog_box:DialogBox = DialogBox()
        self.dialog_box.new_dialog(DEMO_TEXT, border_radius=20)
        
        
    def render(self, display:pygame.surface.Surface):
        self.title[2] = display.blit(self.title[0], self.title[1])
        self.dialog_box.render(display)        
        
        
    def events(self, event:pygame.event.Event):
        self.dialog_box.events(event)
        
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE and self.dialog_box.dialog is None:
                stages.active_stage = stages.main_menu
                
            if event.key == K_d:
                self.dialog_box.new_dialog(DEMO_TEXT, border_radius=20)
        
        
    def update(self):
        self.dialog_box.update(commons.dt)