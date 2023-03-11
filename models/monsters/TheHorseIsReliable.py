from .MonsterBase import MonsterBase


class TheHorseIsReliable(MonsterBase):
    def __init__(self):
        super(TheHorseIsReliable, self).__init__(
            4, 'Конь адедный',
            'Лягает, кусает и жутко воняет. Потеряй 2 уровня.',
            2, 1
        )

    def do_bad_things(self, req, hero):  # он не убежал
        hero["level"] = max(1, hero["level"] - 2)
