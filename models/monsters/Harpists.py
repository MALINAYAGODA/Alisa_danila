from .MonsterBase import MonsterBase


class Harpists(MonsterBase):
    def __init__(self):
        super(Harpists, self).__init__(4, 'Гарпистки',
                                       'Хреново исполняют ужасную музыку. Потеряй 2 уровня.', 2, 1)

    def do_bad_things(self, req, hero):  # он не убежал
        hero["level"] = max(1, hero["level"] - 2)
