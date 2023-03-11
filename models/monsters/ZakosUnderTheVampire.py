from .MonsterBase import MonsterBase


class ZakosUnderTheVampire(MonsterBase):
    def __init__(self):
        super(ZakosUnderTheVampire, self).__init__(
            12, 'Закос под вампира',
            'Загородив выход, рассказывает о себе. Потеряй 3 уровня.',
            3, 1
        )

    def do_bad_things(self, req, hero):  # он не убежал
        hero["level"] = max(1, hero["level"] - 3)
