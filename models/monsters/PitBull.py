from .MonsterBase import MonsterBase


class PitBull(MonsterBase):
    def __init__(self):
        super(PitBull, self).__init__(
            2, 'Питбуль',
            'В зад укушенный герой - позорище. Потеряй 2 уровня.',
            1, 1
        )

    def do_bad_things(self, req, hero):  # он не убежал
        hero["level"] = max(1, hero["level"] - 2)
