from .ArmamentBase import ArmamentBase


class SpikedKnees(ArmamentBase):
    def __init__(self):
        super(SpikedKnees, self).__init__(1, 'Шипастые коленки', 200, 4)

    def use_armament(self, req, hero):  # надеваем достпехи/оружие
        # в отдельную переменную доб бонус
        pass
