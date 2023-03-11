from .ArmamentBase import ArmamentBase


class TreadSandals(ArmamentBase):
    def __init__(self):
        super(TreadSandals, self).__init__(0, 'Сандалеты-протекторы', 700, 4)

    def use_armament(self, req, hero):  # надеваем достпехи/оружие
        # в отдельную переменную доб бонус
        pass
