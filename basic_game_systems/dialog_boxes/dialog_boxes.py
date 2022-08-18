import pygame
from pygame.locals import *
from pygame.event import Event

MARGIN = 10.0
BOX_HEIGHT = 80.0
TEXT_SPEED = 50
DEFAULT_FONT = ("Arial", 12)

class DialogBox():
    def __init__(self,
        box_height: float = BOX_HEIGHT,
        box_margin: float = MARGIN,
        text_speed: float = TEXT_SPEED,
        skip_keys: list[int] = [K_x, K_SPACE, K_RETURN]
    ) -> None:
        self.chars_counter: float = 0.0
        self.dialog_buffer: list[dict] = []
        self.dialog: dict = None
        self.disabled: bool = False
        self.box_height: float = box_height
        self.box_margin: float = box_margin
        self.text_speed: float = text_speed
        self.skip_keys: list[int] = skip_keys
        

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
            box_rect: pygame.Rect
            
            if align == "top":
                box_rect = pygame.draw.rect(surface, background, (self.box_margin, self.box_margin, surface_size[0] - self.box_margin * 2, self.box_height), border_radius=border_radius)
            elif align == "middle":
                box_rect = pygame.draw.rect(surface, background, (self.box_margin, surface_size[1] / 2 - self.box_height / 2, surface_size[0] - self.box_margin * 2, self.box_height), border_radius=border_radius)
            elif align == "bottom":
                box_rect = pygame.draw.rect(surface, background, (self.box_margin, surface_size[1] - self.box_height - self.box_margin, surface_size[0] - self.box_margin * 2, self.box_height), border_radius=border_radius)
                
            if border:
                pygame.draw.rect(surface, border_color, box_rect, border, border_radius)
            
            box_rect_inner_x = box_rect.x + self.box_margin
            box_rect_inner_y = box_rect.y + self.box_margin
            
            if font is None:
                font = pygame.font.SysFont(DEFAULT_FONT[0], DEFAULT_FONT[1])
            
            for line, text in enumerate(text[0:int(self.chars_counter)].split('\n')):
                rendered_text = font.render(text, True, color)
                surface.blit(rendered_text, (box_rect_inner_x, box_rect_inner_y + line * font.get_height()))

        dialog = self.dialog
        dialog.update({"surface": surface})
        aux_render(**dialog)


    def update(self, dt: float):
        if not self.dialog:
            return
            
        if self.chars_counter < len(self.dialog.get("text", 0)):
            self.chars_counter += self.text_speed * dt


    def process_event(self, event: Event):
        if event.type == KEYDOWN and self.dialog:
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