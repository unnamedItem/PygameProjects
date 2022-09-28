import pygame, sys
from pygame.locals import *

from utils import stage


pygame.init()
screen = pygame.display.set_mode((640, 480), DOUBLEBUF)

@stage
def game() -> bool:
    events()
    update()
    render()


def events() -> bool:
    pass


def update() -> None:
    pass


def render() -> None:
    pass


def quit() -> None:
    pygame.quit()
    sys.exit()


game()