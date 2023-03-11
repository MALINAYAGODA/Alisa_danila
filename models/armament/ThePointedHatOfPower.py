from .ArmamentBase import ArmamentBase


class ThePointedHatOfPower(ArmamentBase):
    def __init__(self):
        super(ThePointedHatOfPower, self).__init__(3, 'Остроконечная шляпа могущества', 400, 2)

    def use_armament(self, req, hero):  # надеваем достпехи/оружие
        # в отдельную переменную доб бонус
        pass
