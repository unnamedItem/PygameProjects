class Material():
    def __init__(self, id: int) -> None:
        self.id: int = id
        self.name: str = ""
        self.colour: tuple = (0,0,0,0)
        self.weigth: float = 0.0
        self.hardenness: float = 0.0
        self.flexibility: float = 0.0
        self.properties: list[str] = []
        self.value: float = 0.0