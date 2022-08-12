import pygame, sys, time

from pygame.locals import *
from pygame import Vector2

from constants import *
from dialog_boxes import dialog_box


TEST_TEXT = '\
    Welcome to simple dialog boxes!\n\
    This is a random text dialog.\n\
    \n\
    Goodbye!\
'

class Game():
    def __init__(self, game_name: str) -> None:
        # Pygame Init ------------------------------------- #
        pygame.init()

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
        self.max_ticks = DEFAULT_MAX_TICKS
        self.fps = self.main_clock.get_fps()
        self.fps_display = ''
        self.fps_show = False
        self.fps_changed = False

        # Keys pressed ------------------------------------ #
        self.keys = {
            K_LCTRL: 0,
            K_p: 0,
            KEYUP: 0,
            KEYDOWN: 0
        }
        
        # Text Animation ---------------------------------- #
        self.text_speed = 20
        self.count_chars = 0.0
        self.text_length = len(TEST_TEXT)
        self.text_display = False


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
                    
                if event.key == K_SPACE:
                    self.text_display = not self.text_display

            if event.type == KEYUP:
                self.keys[KEYDOWN] = 0
                self.keys[KEYUP] = 1

                if event.key == K_LCTRL:
                    self.keys[K_LCTRL] = 0

                if event.key == K_p:
                    self.keys[K_p] = 0


    # Update Game ------------------------------- #
    def update(self, dt) -> None:
        self.fps_update()

        if self.keys[K_LCTRL] and self.keys[K_p] and not self.fps_changed:
            self.fps_show = not self.fps_show
            self.fps_changed = True

        if self.keys[KEYUP]:
            self.fps_changed = False
            
        if self.count_chars < self.text_length and self.text_display:
            self.count_chars += self.text_speed * dt


    # Draw Game --------------------------------- #
    def draw(self):
        self.display.fill((30,20,30))

        # Layers ------------------------------------- #
        layer0 = pygame.Surface(self.display.get_size(), SRCALPHA)
        dialog_box(TEST_TEXT[0:int(self.count_chars)], layer0, border_radius=10)
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
        self.main_clock.tick(self.max_ticks)
        self.fps = self.main_clock.get_fps()
        dt = time.time() - self.last_time
        self.last_time = time.time()
        return dt


    # Fps Update -------------------------------- #
    def fps_update(self) -> None:
        fps_str = str(int(self.fps))
        text = self.font.render(fps_str, True, (255, 255, 255))
        self.fps_display = text


    # Fps Render -------------------------------- #
    def fps_render(self, layer: pygame.surface.Surface) -> None:
        if self.fps_show:
            layer.blit(self.fps_display, (self.display_size[0] - self.fps_display.get_size()[0] - 10, 5))


Game(GAME_NAME).run()