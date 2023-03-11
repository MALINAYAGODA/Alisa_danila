from .ArmamentBase import ArmamentBase


class SlimyBarrel(ArmamentBase):
    def __init__(self):
        super(SlimyBarrel, self).__init__(1, 'Слизистая бочка', 200, 3)

    def use_armament(self, req, hero):  # надеваем достпехи/оружие
        # в отдельную переменную доб бонус
        pass
