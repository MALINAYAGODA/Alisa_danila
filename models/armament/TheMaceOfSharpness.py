from .ArmamentBase import ArmamentBase


class TheMaceOfSharpness(ArmamentBase):
    def __init__(self):
        super(TheMaceOfSharpness, self).__init__(4, 'Палица остроты', 600, 1, 1)

    def use_armament(self, req, hero):  # надеваем достпехи/оружие
        # в отдельную переменную доб бонус
        pass
