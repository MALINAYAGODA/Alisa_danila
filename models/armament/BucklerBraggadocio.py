from .ArmamentBase import ArmamentBase


class BucklerBraggadocio(ArmamentBase):
    def __init__(self):
        super(BucklerBraggadocio, self).__init__(2, 'Баклер бахвала', 400, 1, 1)

    def use_armament(self, req, hero):  # надеваем достпехи/оружие
        # в отдельную переменную доб бонус
        pass
