from pygame.surface import Surface
from pygame.event import Event


class Stage:
    def events(self, event:Event) -> None:
        pass

    def update(self) -> None:
        pass

    def render(self, display:Surface) -> None:
        pass
