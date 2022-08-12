import pygame, sys, time

from pygame.locals import *
from pygame import Vector2

from constants import *


class Game():
    def __init__(self, game_name: str) -> None:
        # Pygame Init ------------------------------------- #
        pygame.init()

        # Display Settings -------------------------------- #
        self.scale = 1.5
        self.display_size = Vector2(DISPLAY_SIZE)
        self.screen_size = Vector2(DISPLAY_SIZE) * self.scale
        self.display = pygame.Surface(self.display_size)
        self.screen = pygame.display.set_mode((self.screen_size), DOUBLEBUF, DEFAULT_BPP)
        self.game_name = game_name
        pygame.display.set_caption(game_name)

        # Font -------------------------------------------- #
        self.font_0 = pygame.font.Font('./assets/fonts/Grand9K_Pixel.ttf', 10)
        self.font_1 = pygame.font.Font('./assets/fonts/Grand9K_Pixel.ttf', 12)
        self.font_2 = pygame.font.Font('./assets/fonts/Grand9K_Pixel.ttf', 14)
        self.font_3 = pygame.font.Font('./assets/fonts/Grand9K_Pixel.ttf', 16)
        self.font_4 = pygame.font.Font('./assets/fonts/Grand9K_Pixel.ttf', 18)
        self.font_5 = pygame.font.Font('./assets/fonts/Grand9K_Pixel.ttf', 20)

        # Clock ------------------------------------------- #
        self.main_clock = pygame.time.Clock()
        self.last_time = time.time()
        self.fps = self.main_clock.get_fps()
        self.fps_display = ''
        self.fps_show = False
        self.fps_changed = False

        # Keys pressed ------------------------------------ #
        self.keys = {
            K_LCTRL: 0,
            K_p: 0,
            KEYUP: 0,
            KEYDOWN: 0,
            BUTTON_LEFT: 0,
            BUTTON_RIGHT: 0,
        }
        
        # Mouse ------------------------------------------- #
        self.mouse_x = 0
        self.mouse_y = 0
        
        # Draw Tool --------------------------------------- #
        self.draw_size = (32, 32)
        self.map_data = [ [0 for _ in range(self.draw_size[0])] for _ in range(self.draw_size[1]) ]


    # Run Game ---------------------------------- #
    def run(self) -> None:
        while 1:
            dt = self.delta_time()
            self.process_events()
            self.update(dt)
            self.draw()


    # Handle events ----------------------------- #
    def process_events(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                self.quit()

            if event.type == KEYDOWN:
                self.keys[KEYDOWN] = 1
                self.keys[KEYUP] = 0
                
                if event.key == K_ESCAPE:
                    self.quit()

                if event.key == K_LCTRL:
                    self.keys[K_LCTRL] = 1

                if event.key == K_p:
                    self.keys[K_p] = 1

            if event.type == KEYUP:
                self.keys[KEYDOWN] = 0
                self.keys[KEYUP] = 1

                if event.key == K_LCTRL:
                    self.keys[K_LCTRL] = 0

                if event.key == K_p:
                    self.keys[K_p] = 0
                    
            if event.type == MOUSEBUTTONDOWN:
                if event.button == BUTTON_RIGHT:
                    self.keys[BUTTON_RIGHT] = 1
                
                if event.button == BUTTON_LEFT:
                    self.keys[BUTTON_LEFT] = 1
                    
            if event.type == MOUSEBUTTONUP:
                if event.button == BUTTON_RIGHT:
                    self.keys[BUTTON_RIGHT] = 0
                
                if event.button == BUTTON_LEFT:
                    self.keys[BUTTON_LEFT] = 0


    # Update Game ------------------------------- #
    def update(self, dt) -> None:
        self.fps_update()
        
        self.mouse_x = pygame.mouse.get_pos()[0] / self.scale
        self.mouse_y = pygame.mouse.get_pos()[1] / self.scale

        if self.keys[K_LCTRL] and self.keys[K_p] and not self.fps_changed:
            self.fps_show = not self.fps_show
            self.fps_changed = True

        if self.keys[KEYUP]:
            self.fps_changed = False
            
        if self.keys[BUTTON_LEFT]:
            if 32 <= self.mouse_x < DISPLAY_SIZE[0] - 192 and 32 <= self.mouse_y < DISPLAY_SIZE[1] - 32:
                self.map_data[int((self.mouse_x - 32) / 16)][int((self.mouse_y - 32) / 16)] = 1
                
        if self.keys[BUTTON_RIGHT]:
            if 32 <= self.mouse_x < DISPLAY_SIZE[0] - 192 and 32 <= self.mouse_y < DISPLAY_SIZE[1] - 32:
                self.map_data[int((self.mouse_x - 32) / 16)][int((self.mouse_y - 32) / 16)] = 0


    # Draw Game --------------------------------- #
    def draw(self):
        self.display.fill((30,20,30))

        # Layers ------------------------------------- #
        layer0 = pygame.Surface(self.display.get_size(), SRCALPHA)
        self.fps_render(layer0)
        
        for x in range(32, DISPLAY_SIZE[0] - 176, 16):
            pygame.draw.line(layer0, (140, 140, 140), (x, 32), (x, DISPLAY_SIZE[1] - 32), 1)
        for y in range(32, DISPLAY_SIZE[1] - 16, 16):
            pygame.draw.line(layer0, (140, 140, 140), (32, y), (DISPLAY_SIZE[0] - 192, y), 1)
            
        dx = 0
        for x in self.map_data:
            dy = 0
            for y in x:
                if y == 1:
                    pygame.draw.rect(layer0, (0, 200, 0), (dx * 16 + 33, dy * 16 + 33, 15, 15))
                dy += 1
            dx += 1
            
        pygame.draw.rect(layer0, (140, 14, 14), (int(self.mouse_x / 16) * 16, int(self.mouse_y / 16) * 16, 16, 16), 1)

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
        self.main_clock.tick(60)
        self.fps = self.main_clock.get_fps()
        dt = time.time() - self.last_time
        self.last_time = time.time()
        return dt


    # Fps Update -------------------------------- #
    def fps_update(self) -> None:
        fps_str = str(round(self.fps, 2))
        text = self.font_0.render(fps_str, True, (255, 255, 255))
        self.fps_display = text
        

    # Fps Render -------------------------------- #
    def fps_render(self, layer: pygame.surface.Surface) -> None:
        if self.fps_show:
            layer.blit(self.fps_display, (self.display_size[0] - self.fps_display.get_size()[0] - 10, 5))


Game(GAME_NAME).run()
