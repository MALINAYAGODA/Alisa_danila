from .ArmamentBase import ArmamentBase


class HornedHelmet(ArmamentBase):
    def __init__(self):
        super(HornedHelmet, self).__init__(1, 'Шлем рогач', 600, 2)

    def use_armament(self, req, hero):  # надеваем достпехи/оружие
        # в отдельную переменную доб бонус
        pass
