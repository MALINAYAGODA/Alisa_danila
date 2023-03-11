from .MonsterBase import MonsterBase


class TheCrippledGoblin(MonsterBase):
    def __init__(self):
        super(TheCrippledGoblin, self).__init__(
            1, 'Увечный гоблин',
            'Лупцует тебя костылём. Потеряй уровень.',
            1, 1
        )

    def do_bad_things(self, req, hero):  # он не убежал
        hero["level"] = max(1, hero["level"] - 1)
