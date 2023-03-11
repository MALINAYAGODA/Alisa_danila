from .ArmamentBase import ArmamentBase


class AnElevenFootPole(ArmamentBase):
    def __init__(self):
        super(AnElevenFootPole, self).__init__(1, 'Одиннадцатифутовый шест', 200, 1, 2)

    def use_armament(self, req, hero):  # надеваем достпехи/оружие
        # в отдельную переменную доб бонус
        pass
