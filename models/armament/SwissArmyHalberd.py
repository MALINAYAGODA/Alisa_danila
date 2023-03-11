from .ArmamentBase import ArmamentBase


class SwissArmyHalberd(ArmamentBase):
    def __init__(self):
        super(SwissArmyHalberd, self).__init__(4, 'Швейцарская армейская алебарда', 600, 1, 2)

    def use_armament(self, req, hero):  # надеваем достпехи/оружие
        # в отдельную переменную доб бонус
        pass
