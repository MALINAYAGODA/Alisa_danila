from .BonusBase import BonusBase


class PotionOfGeneralCoolness(BonusBase):
    def __init__(self):
        super(PotionOfGeneralCoolness, self).__init__(
            'Зелье общей крутизны',
            'Зелье общей крутизны',
            1000,
            'Получи уровень.'
        ) # получи уровень

    def use_bonus(self, req, hero):  # используем бонус, улучшаем героя
        hero["level"] += 1
