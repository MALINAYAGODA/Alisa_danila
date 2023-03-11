from .MonsterBase import MonsterBase


class PaganDemon(MonsterBase):
    def __init__(self):
        super(PaganDemon, self).__init__(
            12, 'Языческий демон',
            'Отвратительный поцелуй лишает тебя двух (а если ты эльф - трех) уровней.',
            3, 1
        )

    def do_bad_things(self, req, hero):  # он не убежал
        hero["level"] = max(1, hero["level"] - 2)
