from .ArmamentBase import ArmamentBase


class SwordOfSongAndDance(ArmamentBase):
    def __init__(self):
        super(SwordOfSongAndDance, self).__init__(2, 'Меч песен и пляски', 400, 1)

    def use_armament(self, req, hero):  # надеваем достпехи/оружие
        # в отдельную переменную доб бонус
        pass
