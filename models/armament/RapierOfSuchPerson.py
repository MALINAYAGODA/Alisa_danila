from .ArmamentBase import ArmamentBase


class RapierOfSuchPerson(ArmamentBase):
    def __init__(self):
        super(RapierOfSuchPerson, self).__init__(3, 'Рапира такнечестности', 600, 1, 1)

    def use_armament(self, req, hero):  # надеваем достпехи/оружие
        # в отдельную переменную доб бонус
        pass
