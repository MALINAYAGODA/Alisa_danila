from .MonsterBase import MonsterBase


class FlyingFrogs(MonsterBase):
    def __init__(self):
        super(FlyingFrogs, self).__init__(2, 'Летучие лягушки',
                                          'Острые легушачьи клыки сгрызают с тебя 2 уровня.', 1, 1)

    def do_bad_things(self, req, hero):  # он не убежал
        hero["level"] = max(1, hero["level"] - 2)
