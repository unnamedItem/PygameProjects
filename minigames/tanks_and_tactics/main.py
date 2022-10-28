from os import listdir
from posixpath import abspath
import pygame, sys, time, random

from pygame.locals import *
from pygame import Vector2

from constants import *


class Game():
    def __init__(self) -> None:
        # Pygame Init ------------------------------------- #
        pygame.init()
        pygame.mouse.set_visible(False)

        # Display Settings -------------------------------- #
        self.display_size = Vector2(DISPLAY_SIZE)
        self.screen_size_list = [size for size in pygame.display.list_modes() if size[0] > self.display_size[0] and size[1] > self.display_size[1]]
        self.screen_size = self.screen_size_list[12]
        self.scale = self.screen_size[0] / self.display_size[0] if (self.screen_size[0] / self.display_size[0]) < (self.screen_size[1] / self.display_size[1]) else self.screen_size[1] / self.display_size[1]
        self.display = pygame.Surface(self.display_size)
        self.screen = pygame.display.set_mode((self.screen_size), DOUBLEBUF, DEFAULT_BPP)
        self.game_name = GAME_NAME
        pygame.display.set_caption(self.game_name)
        
        # Font -------------------------------------------- #
        self.font = pygame.font.SysFont('verdana', 12)

        # Clock ------------------------------------------- #
        self.main_clock = pygame.time.Clock()
        self.last_time = time.time()
        self.fps = self.main_clock.get_fps()
        self.fps_display = ''
        self.fps_show = True

        # System HUI
        self.cursor_pos = Vector2(0,0)
        self.cursor_img = 'cursor'
        self.system_assets = { key[:-4]: pygame.image.load(abspath('') + '/assets/system/' + key) for key in listdir(abspath('') + '/assets/system') }
        self.menu_rects = []
        self.acctions_selected = []

        # Tile Map
        #self.tile_map = [ [ random.choice([0,0] + [1 for _ in range(x%2 + y%3)]) for x in range(16) ] for y in range(16) ]
        self.tile_map = [ [ x%2 + y%2 for x in range(16) ] for y in range(16) ]
        #for y1, y2, dx in [(0, 2, 0), (0, 2, 2), (14, 16, 0), (14, 16, 2)]:
        #    for row in self.tile_map[y1:y2]:
        #        for x in range(2):
        #            row[x - dx] = 0

        # Player
        self.player_rect = pygame.Rect(324,324, 12, 12)

        # Acctions
        self.execute_acctions = False
        self.acction = None
        self.move_count = 0
        self.bullets = []


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

            if self.execute_acctions:
                return

            if event.type == MOUSEBUTTONDOWN:
                if event.button == BUTTON_LEFT:
                    for rect, btn in self.menu_rects:
                        if pygame.Rect.colliderect(rect, (self.cursor_pos[0], self.cursor_pos[1], 1, 1)):
                            if "slot" in btn:
                                if len(self.acctions_selected) > int(btn[5:]):
                                    self.acctions_selected.pop(int(btn[5:]))
                            elif btn == "start":
                                self.execute_acctions = True
                            elif len(self.acctions_selected) < 10:
                                self.acctions_selected.append(btn)


    # Update Game ------------------------------- #
    def update(self, dt) -> None:
        self.cursor_pos = (Vector2(pygame.mouse.get_pos() - Vector2((self.screen_size[0] - self.display_size[0] * self.scale) / 2,0)) / self.scale) 
        self.fps_update()

        if self.execute_acctions:
            if not self.acction and self.acctions_selected:
                self.acction = self.acctions_selected.pop(0)
            elif not self.acctions_selected and not self.acction:
                self.execute_acctions = False
            elif self.acction:
                if "arrow" in self.acction:
                    self.move_count += 1
                    if self.move_count == 21:
                        self.move_count = 0
                        self.acction = None
                    elif "top" in self.acction:
                        self.player_rect.y -= 1
                    elif "bottom" in self.acction:
                        self.player_rect.y += 1
                    elif "left" in self.acction:
                        self.player_rect.x -= 1
                    elif "right" in self.acction:
                        self.player_rect.x += 1
                else:
                    if "top" in self.acction:
                        self.bullets.append([Vector2(0,-2), Vector2(self.player_rect.center)])
                    elif "bottom" in self.acction:
                        self.bullets.append([Vector2(0,2), Vector2(self.player_rect.center)])
                    elif "left" in self.acction:
                        self.bullets.append([Vector2(-2,0), Vector2(self.player_rect.center)])
                    elif "right" in self.acction:
                        self.bullets.append([Vector2(2,0), Vector2(self.player_rect.center)])
                    self.acction = None

        for bullet in self.bullets:
            bullet[1] = bullet[1] + bullet[0]



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

        menu_arrows = ["arrow_top", "arrow_bottom", "arrow_left", "arrow_right"]
        menu_shoot = ["shoot_top", "shoot_bottom", "shoot_left", "shoot_right"]
        menu_rects = []
        
        for idx, img_name in enumerate(menu_arrows):
            menu_rects.append((layer0.blit(self.system_assets[img_name], (362 + idx * 25,20)), img_name))
        for idx, img_name in enumerate(menu_shoot):
            menu_rects.append((layer0.blit(self.system_assets[img_name], (362 + idx * 25,50)), img_name))

        for row in range(2):
            for idx in range(5):
                menu_rects.append((pygame.draw.rect(layer0, (120,130,120), (354 + idx*22, 80 + row*22, 22, 22), 1, -1), 'slot-' + str(idx + row*5)))

        menu_rects.append((pygame.draw.rect(layer0, (179, 186, 205), (360, 320, 100, 20), border_radius=10), 'start'))
        pygame.draw.rect(layer0, (79,85,105), (360, 320, 100, 20), 1, border_radius=10)
        start_text = self.font.render("RUN", True, (79,85,105))
        layer0.blit(start_text, (410 - start_text.get_width() / 2, 330 - start_text.get_height() / 2))

        for idx, acction in enumerate(self.acctions_selected):
            layer0.blit(self.system_assets[acction], (355 + (idx%5)*22, 81 + 22*(int(idx/5))))

        self.menu_rects = menu_rects

        pygame.draw.rect(layer0, (255,0,0), self.player_rect)

        for bullet in self.bullets:
            pygame.draw.rect(layer0, (255, 255, 255), (bullet[1][0] - 2, bullet[1][1] - 2, 4, 4))

        self.cursor_img = "cursor"
        for rect, _ in menu_rects:
            if pygame.Rect.colliderect(rect, (self.cursor_pos[0], self.cursor_pos[1], 1, 1)):
                self.cursor_img = 'finger'

        layer0.blit(self.system_assets[self.cursor_img], self.cursor_pos)
        self.fps_render(layer0)

        # Blit Layers -------------------------------- #
        self.display.blit(layer0, Vector2())

        self.screen.fill((30,20,30))
        self.screen.blit(pygame.transform.scale(self.display, self.display_size * self.scale), ((self.screen_size[0] - self.display_size[0] * self.scale) / 2,0))
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
            layer.blit(self.fps_display, (self.display_size[0] - 40, 0))


Game().run()
