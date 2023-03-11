from .ArmamentBase import ArmamentBase


class TheShoesOfTheMightyPendel(ArmamentBase):
    def __init__(self):
        super(TheShoesOfTheMightyPendel, self).__init__(2, 'Башмаки могучего пенделя', 400, 4)

    def use_armament(self, req, hero):  # надеваем достпехи/оружие
        # в отдельную переменную доб бонус
        pass
