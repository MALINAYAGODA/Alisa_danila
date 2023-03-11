from .ArmamentBase import ArmamentBase


class BowWithRibbons(ArmamentBase):
    def __init__(self):
        super(BowWithRibbons, self).__init__(4, 'Лучок с ленточками', 800, 1, 2)

    def use_armament(self, req, hero):  # надеваем достпехи/оружие
        # в отдельную переменную доб бонус
        pass
