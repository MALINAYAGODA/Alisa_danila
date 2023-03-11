from .ArmamentBase import ArmamentBase


class TightsOfGiantStrength(ArmamentBase):
    def __init__(self):
        super(TightsOfGiantStrength, self).__init__(3, 'Колготы великанской силы', 600, 4)

    def use_armament(self, req, hero):  # надеваем достпехи/оружие
        # в отдельную переменную доб бонус
        pass
