WEAPON_RARITY = dict(list(enumerate(iterable=("Common", "Uncommon", "Rare", "Mythic", "Epic", "Legendary", "Unique"))))
DEFAULT_PIXEL_MAP_SIZE = (32, 32)
MAP_ID = 0
MATERIAL_ID = 1

class Weapon():
    def __init__(self, id: int) -> None:
        self.id: int = id
        self.name: str = ""
        self.rarity: str = WEAPON_RARITY[0]
        self.pixel_map_size: tuple = DEFAULT_PIXEL_MAP_SIZE
        self.pixel_map: list[list[int]] = [ [ [0, 0] for _ in range(self.pixel_map_size[0]) ] for _ in range(self.pixel_map_size[1]) ]
        self.pixel_ids: dict = {"0": "non-drawbable"}


class Sword(Weapon):
    def __init__(self, id: int) -> None:
        super().__init__(id)
        self.pixel_ids.update(dict(list(enumerate(iterable=("blade", "hilt"), start=1))))

weapon = Sword(1)
print(weapon.pixel_map)
