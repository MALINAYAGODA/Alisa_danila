from .MonsterBase import MonsterBase


class Bulldog(MonsterBase):
    def __init__(self):
        super(Bulldog, self).__init__(18, 'Бульрог', 'Ты запорот до смерти.', 5, 2)

    def do_bad_things(self, req, hero):  # он не убежал
        hero["is_alive"] = False
