from .ArmamentBase import ArmamentBase


class Chainsaw(ArmamentBase):
    def __init__(self):
        super(Chainsaw, self).__init__(3, 'Бензопила', 600, 1, 2)

    def use_armament(self, req, hero):  # надеваем достпехи/оружие
        # в отдельную переменную доб бонус
        pass
