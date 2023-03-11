from .RaceBase import RaceBase


class Elf(RaceBase):
    def __init__(self):
        super().__init__(1, 'Эльфы очень удачливые существа! +1 к смывке!')