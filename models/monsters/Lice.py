from .MonsterBase import MonsterBase


class Lice(MonsterBase):
    def __init__(self):
        super(Lice, self).__init__(
            1, 'Вошки',
            'Сбрось броник и все шмотки, надетые ниже пояса.',
            1, 1
        )

    def do_bad_things(self, req, hero):  # он не убежал
        hero["armor"]["leg"] = None
