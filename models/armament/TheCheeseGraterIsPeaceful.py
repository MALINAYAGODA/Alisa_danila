from .ArmamentBase import ArmamentBase


class TheCheeseGraterIsPeaceful(ArmamentBase):
    def __init__(self):
        super(TheCheeseGraterIsPeaceful, self).__init__(3, 'Сыротёрка умиротворенная', 400, 1, 1)

    def use_armament(self, req, hero):  # надеваем достпехи/оружие
        # в отдельную переменную доб бонус
        pass
