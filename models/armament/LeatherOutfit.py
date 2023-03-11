from .ArmamentBase import ArmamentBase


class LeatherOutfit(ArmamentBase):
    def __init__(self):
        super(LeatherOutfit, self).__init__(1, 'Кожаный прикид', 200, 3)

    def use_armament(self, req, hero):  # надеваем достпехи/оружие
        # в отдельную переменную доб бонус
        pass
