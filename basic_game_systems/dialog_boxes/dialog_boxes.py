import pygame

MARGIN = 10
BOX_HEIGHT = 80
DEFAULT_FONT = ("Arial", 12)

def dialog_box(
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
        box_rect = pygame.draw.rect(surface, background, (MARGIN, MARGIN, surface_size[0] - MARGIN * 2, BOX_HEIGHT), border_radius=border_radius)
    elif align == "middle":
        box_rect = pygame.draw.rect(surface, background, (MARGIN, surface_size[1] / 2 - BOX_HEIGHT / 2, surface_size[0] - MARGIN * 2, BOX_HEIGHT), border_radius=border_radius)
    elif align == "bottom":
        box_rect = pygame.draw.rect(surface, background, (MARGIN, surface_size[1] - BOX_HEIGHT - MARGIN, surface_size[0] - MARGIN * 2, BOX_HEIGHT), border_radius=border_radius)
        
    pygame.draw.rect(surface, border_color, box_rect, border, border_radius)
    
    box_rect_inner_x = box_rect.x + MARGIN
    box_rect_inner_y = box_rect.y + MARGIN
    
    if font is None:
        font = pygame.font.SysFont(DEFAULT_FONT[0], DEFAULT_FONT[1])
    
    for line, text in enumerate(text.split('\n')):
        rendered_text = font.render(text, True, color)
        surface.blit(rendered_text, (box_rect_inner_x, box_rect_inner_y + line * font.get_height()))
    
