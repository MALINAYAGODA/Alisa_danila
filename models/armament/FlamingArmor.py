from .ArmamentBase import ArmamentBase


class FlamingArmor(ArmamentBase):
    def __init__(self):
        super(FlamingArmor, self).__init__(2, 'Пламенные латы', 400, 3)

    def use_armament(self, req, hero):  # надеваем достпехи/оружие
        # в отдельную переменную доб бонус
        pass
