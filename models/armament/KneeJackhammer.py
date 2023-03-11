from .ArmamentBase import ArmamentBase


class KneeJackhammer(ArmamentBase):
    def __init__(self):
        super(KneeJackhammer, self).__init__(4, 'Коленоотбоный молот', 600, 1, 1)

    def use_armament(self, req, hero):  # надеваем достпехи/оружие
        # в отдельную переменную доб бонус
        pass
