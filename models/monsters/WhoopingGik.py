from .MonsterBase import MonsterBase


class WhoopingGik(MonsterBase):
    def __init__(self):
        super(WhoopingGik, self).__init__(6, 'Гикающий Гик', 'Стань нормальным. Потеряй расу', 2, 1)

    def do_bad_things(self, req, hero):  # он не убежал
        pass
