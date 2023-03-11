from .ArmamentBase import ArmamentBase


class KorotyshirokneArmor(ArmamentBase):
    def __init__(self):
        super(KorotyshirokneArmor, self).__init__(3, 'Коротыширокне латы', 400, 3)

    def use_armament(self, req, hero):  # надеваем достпехи/оружие
        # в отдельную переменную доб бонус
        pass
