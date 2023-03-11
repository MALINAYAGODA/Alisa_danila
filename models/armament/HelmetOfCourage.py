from .ArmamentBase import ArmamentBase



class HelmetOfCourage(ArmamentBase):
    def __init__(self):
        super(HelmetOfCourage, self).__init__(1, 'Шлем отваги', 200, 2)

    def use_armament(self, req, hero):  # надеваем достпехи/оружие
        # в отдельную переменную доб бонус
        pass
