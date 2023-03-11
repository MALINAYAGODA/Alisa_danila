from .MonsterBase import MonsterBase


class Burp(MonsterBase):
    def __init__(self):
        super(Burp, self).__init__(6, 'Рыгачу', 'Рвота, в атаку! Придётся сбросить всю руку.', 2, 1)

    def do_bad_things(self, req, hero):  # он не убежал
        if len(hero["weapon"] > 0):
            del hero["weapon"][0]
