from .MonsterBase import MonsterBase


class Utconticore(MonsterBase):
    def __init__(self):
        super(Utconticore, self).__init__(6, 'Утконтикора', 'Потеряй 2 уровня.', 2, 1)

    def do_bad_things(self, req, hero):  # он не убежал
        hero["level"] = max(1, hero["level"] - 2)
