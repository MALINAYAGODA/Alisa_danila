from .MonsterBase import MonsterBase


class Mademoiselle(MonsterBase):
    def __init__(self):
        super(Mademoiselle, self).__init__(8, 'Мадемонуазели', 'Твой уровень падает до 1.', 2, 1)

    def do_bad_things(self, req, hero):  # он не убежал
        hero["level"] = 1
