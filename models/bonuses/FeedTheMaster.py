from .BonusBase import BonusBase


class FeedTheMaster(BonusBase):
    def __init__(self):
        super(FeedTheMaster, self).__init__(
            'Закорми мастера',
            'Закорми мастера',
            1000,
            'Получи уровень.'
        ) # получи уровень

    def use_bonus(self, req, hero):  # используем бонус, улучшаем героя
        hero["level"] += 1
