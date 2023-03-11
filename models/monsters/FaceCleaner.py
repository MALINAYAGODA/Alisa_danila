from .MonsterBase import MonsterBase


class FaceCleaner(MonsterBase):
    def __init__(self):
        super(FaceCleaner, self).__init__(
            8, 'Лицесос',
            'Усердно ссасывает с тебя лицо. Потеряй надетый головняк и уровень.',
            2, 1
        )

    def do_bad_things(self, req, hero):  # он не убежал
        hero["level"] = max(1, hero["level"] - 1)
        hero["armor"]["head"] = None
