from .MonsterBase import MonsterBase


class PaleBrothers(MonsterBase):
    def __init__(self):
        super(PaleBrothers, self).__init__(16, 'Бледные братья', 'Вернись на 1-ый уровень.', 4, 2)

    def do_bad_things(self, req, hero):  # он не убежал
        hero["level"] = 1
