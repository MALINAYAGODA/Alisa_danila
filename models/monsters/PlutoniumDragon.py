from .MonsterBase import MonsterBase


class PlutoniumDragon(MonsterBase):
    def __init__(self):
        super(PlutoniumDragon, self).__init__(
            20, 'Плутониевый дракон',
            'Ты зажарен и съеден. Это верная смерть.',
            5, 2
        )

    def do_bad_things(self, req, hero):  # он не убежал
        hero["is_alive"] = False
