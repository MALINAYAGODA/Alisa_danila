from .MonsterBase import MonsterBase


class CucumberGrass(MonsterBase):
    def __init__(self):
        super(CucumberGrass, self).__init__(1, 'Огоршённая трава', 'Нет. Смывка автоматическая', 1, 1)

    def do_bad_things(self, req, hero):  # он не убежал
        pass
