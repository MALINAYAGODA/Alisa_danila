from .ArmamentBase import ArmamentBase

class HugeStone(ArmamentBase):
    def __init__(self):
        super(HugeStone, self).__init__(3, 'Огромный камень', 400, 1, 2)

    def use_armament(self, req, hero):  # надеваем достпехи/оружие
        # в отдельную переменную доб бонус
        pass
