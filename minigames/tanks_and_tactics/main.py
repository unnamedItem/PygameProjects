from os import listdir
from posixpath import abspath
import pygame, sys, time

from pygame.locals import *
from pygame import Vector2

from constants import *


class Game():
    def __init__(self, game_name: str) -> None:
        # Pygame Init ------------------------------------- #
        pygame.init()
        pygame.mouse.set_visible(False)

        # Display Settings -------------------------------- #
        self.scale = 2
        self.display_size = Vector2(DISPLAY_SIZE)
        self.screen_size = Vector2(DISPLAY_SIZE) * self.scale
        self.display = pygame.Surface(self.display_size)
        self.screen = pygame.display.set_mode((self.screen_size), DOUBLEBUF, DEFAULT_BPP)
        self.game_name = game_name
        pygame.display.set_caption(game_name)

        # Font -------------------------------------------- #
        self.font = pygame.font.SysFont('verdana', 10)

        # Clock ------------------------------------------- #
        self.main_clock = pygame.time.Clock()
        self.last_time = time.time()
        self.fps = self.main_clock.get_fps()
        self.fps_display = ''
        self.fps_show = True

        # System HUI
        self.cursor_pos = Vector2(0,0)
        self.system_assets = { key[:-4]: pygame.image.load(abspath('') + '/assets/system/' + key) for key in listdir(abspath('') + '/assets/system') }


    # Run Game ---------------------------------- #
    def run(self) -> None:
        while 1:
            dt = self.delta_time()
            self.process_events()
            self.update(dt)
            self.draw()


    # Handle events ----------------------------- #
    def process_events(self) -> None:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == QUIT:
                self.quit()

            if event.type == KEYDOWN:                   
                if event.key == K_ESCAPE:
                    self.quit()

                if event.key == K_p and keys[K_LCTRL]:
                    self.fps_show = not self.fps_show


    # Update Game ------------------------------- #
    def update(self, dt) -> None:
        self.cursor_pos = Vector2(pygame.mouse.get_pos()) / self.scale
        self.fps_update()


    # Draw Game --------------------------------- #
    def draw(self):
        self.display.fill((30,20,30))

        # Layers ------------------------------------- #
        layer0 = pygame.Surface(self.display.get_size(), SRCALPHA)
        layer0.blit(self.system_assets["cursor"], self.cursor_pos)
        self.fps_render(layer0)

        # Blit Layers -------------------------------- #
        self.display.blit(layer0, Vector2())

        pygame.transform.scale(self.display, self.screen.get_size(), self.screen)
        pygame.display.flip()


    # Exit Game --------------------------------- #
    def quit(self) -> None:
        pygame.quit()
        sys.exit()


    # Delta Time -------------------------------- #
    def delta_time(self) -> float:
        self.main_clock.tick(144)
        self.fps = self.main_clock.get_fps()
        dt = time.time() - self.last_time
        self.last_time = time.time()
        return dt


    # Fps Update -------------------------------- #
    def fps_update(self) -> None:
        fps_str = str(round(self.fps, 2))
        text = self.font.render(fps_str, True, (255, 255, 255))
        self.fps_display = text


    # Fps Render -------------------------------- #
    def fps_render(self, layer: pygame.surface.Surface) -> None:
        if self.fps_show:
            layer.blit(self.fps_display, (self.display_size[0] - 40, 5))


Game(GAME_NAME).run()
