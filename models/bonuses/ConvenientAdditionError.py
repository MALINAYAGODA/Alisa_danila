from .BonusBase import BonusBase


class ConvenientAdditionError(BonusBase):
    def __init__(self):
        super(ConvenientAdditionError, self).__init__(
            'Удобная ошибка при сложении',
            'Удобная ошибка при сложении',
            1000,
            'Получи уровень.'
        ) # получи уровень

    def use_bonus(self, req, hero):  # используем бонус, улучшаем героя
        hero["level"] += 1
