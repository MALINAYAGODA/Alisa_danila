from .ArmamentBase import ArmamentBase


class TheDaggerOfTreason(ArmamentBase):
    def __init__(self):
        super(TheDaggerOfTreason, self).__init__(3, 'Кинжал измены', 400, 1, 1)

    def use_armament(self, req, hero):  # надеваем достпехи/оружие
        # в отдельную переменную доб бонус
        pass
