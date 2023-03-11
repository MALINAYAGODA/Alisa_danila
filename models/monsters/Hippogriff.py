from .MonsterBase import MonsterBase
from random import choice


class Hippogriff(MonsterBase):
    def __init__(self):
        super(Hippogriff, self).__init__(
            16, 'Гиппогриф',
            'Ты потоптан и покусан, да еще растерял шмот. Потеряй один уровень и рандомно один шмот',
            4, 2
        )

    def do_bad_things(self, req, hero):  # он не убежал
        hero["level"] = max(1, hero["level"] - 1)
        hero["armor"][choice(list(hero["armor"].keys()))] = None
