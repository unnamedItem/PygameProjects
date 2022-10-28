import pygame
from pygame.locals import *
from pygame.event import Event

MARGIN = 10.0
BOX_HEIGHT = 80.0
TEXT_SPEED = 50
DEFAULT_FONT = ("Arial", 12)
TEXT_THRESHOLD = 2

class DialogBox():
    def __init__(self,
        box_height: float = BOX_HEIGHT,
        box_margin: float = MARGIN,
        text_speed: float = TEXT_SPEED,
        skip_keys: 'list[int]' = [K_x, K_SPACE, K_RETURN]
    ) -> None:
        self.chars_counter: float = 0.0
        self.dialog_buffer: list[dict] = []
        self.dialog: dict = None
        self.disabled: bool = False
        self.box_height: float = box_height
        self.box_margin: float = box_margin
        self.skip_keys: list[int] = skip_keys
        self.text_speed: float = text_speed
        self.text_pos_y: float = 0.0
        
        self.box_rect: pygame.Rect = None
        self.text_rect: pygame.Rect = None
        

    def render(self, surface: pygame.Surface) -> None:
        if not self.dialog or self.disabled:
            return

        def aux_render(
            text: str,
            surface: pygame.Surface,
            align: str = "bottom",
            font: pygame.font.Font = None,
            color: tuple = (255, 255, 255, 255),
            background: tuple = (0, 0, 0, 255),
            border: int = 1,
            border_color: tuple = (255, 255, 255, 255),
            border_radius: int = -1
        ) -> None:
            surface_size = surface.get_size()
            
            if not self.box_rect:        
                if align == "top":
                    self.box_rect = pygame.Rect(self.box_margin, self.box_margin, surface_size[0] - self.box_margin * 2, self.box_height)
                elif align == "middle":
                    self.box_rect = pygame.Rect(self.box_margin, surface_size[1] / 2 - self.box_height / 2, surface_size[0] - self.box_margin * 2, self.box_height)
                elif align == "bottom":
                    self.box_rect = pygame.Rect(self.box_margin, surface_size[1] - self.box_height - self.box_margin, surface_size[0] - self.box_margin * 2, self.box_height)
                
            pygame.draw.rect(surface, background, self.box_rect, border_radius=border_radius)
            if border:
                pygame.draw.rect(surface, border_color, self.box_rect, border, border_radius)
            
            box_rect_inner_x = self.box_rect.x + self.box_margin
            box_rect_inner_y = self.box_rect.y + self.box_margin
            
            if font is None:
                font = pygame.font.SysFont(DEFAULT_FONT[0], DEFAULT_FONT[1])
            
            text_layer = pygame.Surface((self.box_rect.width - self.box_margin * 2, len(text.split('\n')) * font.get_height() + TEXT_THRESHOLD), SRCALPHA)
            text_by_line = text[0:int(self.chars_counter)].split('\n')
            for line, text in enumerate(text_by_line):
                rendered_text = font.render(text, True, color)
                text_layer.blit(rendered_text, (-10, line * font.get_height()))
                
            text_current_height = len(text_by_line) * font.get_height() + self.box_margin * 2 + TEXT_THRESHOLD
            if self.text_pos_y < 0 or text_current_height < self.box_height:
                self.text_pos_y = 0
            elif self.text_pos_y > text_current_height - self.box_height:
                self.text_pos_y = text_current_height - self.box_height

            surface.blit(text_layer, (box_rect_inner_x, box_rect_inner_y), (0, self.text_pos_y, self.box_rect.width - self.box_margin * 2, self.box_rect.height - self.box_margin * 2))

        dialog = self.dialog
        dialog.update({"surface": surface})
        aux_render(**dialog)


    def update(self, dt: float):
        if not self.dialog or self.disabled:
            return
            
        if self.chars_counter < len(self.dialog.get("text", 0)):
            self.chars_counter += self.text_speed * dt
            
        keys = pygame.key.get_pressed()
        if self.chars_counter >= len(self.dialog.get("text", 0)):
            if keys[K_UP]:
                self.text_pos_y -= 2
            if keys[K_DOWN]:
                self.text_pos_y += 2


    def process_event(self, event: Event):
        if event.type == KEYDOWN and self.dialog and not self.disabled:
            if event.key in self.skip_keys and self.chars_counter >= len(self.dialog.get("text", 0)):
                if self.dialog_buffer:
                    self.dialog = self.dialog_buffer.pop()
                else:
                    self.dialog = None
                self.chars_counter = 0
            elif event.key in self.skip_keys:
                self.chars_counter = len(self.dialog["text"])

    def new_dialog(self,
        text: str,
        align: str = "bottom",
        font: pygame.font.Font = None,
        color: tuple = (255, 255, 255, 255),
        background: tuple = (0, 0, 0, 255),
        border: int = 1,
        border_color: tuple = (255, 255, 255, 255),
        border_radius: int = -1
    ) -> None:
        varnames, varvalues = list(self.new_dialog.__code__.co_varnames), locals()
        dialog = { key: varvalues.get(key) for key in varnames[1:-2] }
        if self.dialog:
            self.dialog_buffer += [dialog]
        else:
            self.dialog = dialog