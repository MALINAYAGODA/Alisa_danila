from .MonsterBase import MonsterBase


class UnspeakablyTerribleIndescribableHorror(MonsterBase):
    def __init__(self):
        super(UnspeakablyTerribleIndescribableHorror, self).__init__(
            14, 'Невыразимо жуткий неописуемый ужас',
            'Невыразимо жуткая смерть для всех, кто проиграл ему, кроме Хафлингов.',
            4, 1
        )

    def do_bad_things(self, req, hero):  # он не убежал
        hero["is_alive"] = False
