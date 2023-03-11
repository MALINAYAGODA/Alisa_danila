from .ArmamentBase import ArmamentBase


class AirShield(ArmamentBase):
    def __init__(self):
        super(AirShield, self).__init__(4, 'Вездешний щит', 600, 1, 1)

    def use_armament(self, req, hero):  # надеваем достпехи/оружие
        # в отдельную переменную доб бонус
        pass
