from .ArmamentBase import ArmamentBase


class NapalmStaff(ArmamentBase):
    def __init__(self):
        super(NapalmStaff, self).__init__(5, 'Посох напалма', 800, 1, 1)

    def use_armament(self, req, hero):  # надеваем достпехи/оружие
        # в отдельную переменную доб бонус
        pass
