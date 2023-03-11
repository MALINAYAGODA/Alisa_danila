from .ArmamentBase import ArmamentBase


class GentlemenIsOak(ArmamentBase):
    def __init__(self):
        super(GentlemenIsOak, self).__init__(3, 'Дуб джентельменов', 400, 1, 1)

    def use_armament(self, req, hero):  # надеваем достпехи/оружие
        # в отдельную переменную доб бонус
        pass
