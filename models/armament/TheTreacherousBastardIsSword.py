from .ArmamentBase import ArmamentBase


class TheTreacherousBastardIsSword(ArmamentBase):
    def __init__(self):
        super(TheTreacherousBastardIsSword, self).__init__(2, 'Меч коварного ублюдка', 400, 1, 1)

    def use_armament(self, req, hero):  # надеваем достпехи/оружие
        # в отдельную переменную доб бонус
        pass
