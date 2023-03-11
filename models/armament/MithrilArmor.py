from .ArmamentBase import ArmamentBase



class MithrilArmor(ArmamentBase):
    def __init__(self):
        super(MithrilArmor, self).__init__(3, 'Мифрильная броня', 600, 3)

    def use_armament(self, req, hero):  # надеваем достпехи/оружие
        # в отдельную переменную доб бонус
        pass
