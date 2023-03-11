from random import choice
from .MonsterBase import MonsterBase



class Leprechaun(MonsterBase):
    def __init__(self):
        super(Leprechaun, self).__init__(4, 'Лепрокон', 'Забирает у тебя рандомную шмотку.', 2, 1)

    def do_bad_things(self, req, hero):  # он не убежал
        hero["armor"][choice(hero["armor"].keys())] = None
