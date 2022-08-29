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

        # Tile Map
        #self.tile_map = [ [ random.choice([0,0] + [1 for _ in range(x%2 + y%3)]) for x in range(16) ] for y in range(16) ]
        self.tile_map = [ [ x%2 + y%2 for x in range(16) ] for y in range(16) ]
        #for y1, y2, dx in [(0, 2, 0), (0, 2, 2), (14, 16, 0), (14, 16, 2)]:
        #    for row in self.tile_map[y1:y2]:
        #        for x in range(2):
        #            row[x - dx] = 0



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
        pygame.draw.rect(layer0, (0,0,0), (20,20,320,320), 0, -1)
        pygame.draw.rect(layer0, (60,80,65), (18,18,324,324), 2, -1)
        for y, row in enumerate(self.tile_map):
            for x, tile in enumerate(row):
                if tile == 1:
                    pygame.draw.rect(layer0, (150, 150, 120), (20 + (20 * x), 20 + (20 * y), 20, 20))
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
