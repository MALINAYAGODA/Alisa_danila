from .ArmamentBase import ArmamentBase


class TheCloakOfTurbidity(ArmamentBase):
    def __init__(self):
        super(TheCloakOfTurbidity, self).__init__(4, 'Плащ замутненности', 600, 3)

    def use_armament(self, req, hero):  # надеваем достпехи/оружие
        # в отдельную переменную доб бонус
        pass
