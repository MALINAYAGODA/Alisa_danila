from .MonsterBase import MonsterBase


class Bigfoot(MonsterBase):
    def __init__(self):
        super(Bigfoot, self).__init__(12, 'Бигфут',
                                      'Наступает на тебя и съедает шляпу. Потеряй надетый головняк.',
                                      3, 1)

    def do_bad_things(self, req, hero):  # он не убежал
        hero["armor"]["head"] = None
