from .BonusBase import BonusBase


class Gold1000(BonusBase):
    def __init__(self):
        super(Gold1000, self).__init__(
            '1000 Голдов',
            '1000 Голдов',
            1000,
            'Получи уровень.'
        )

    def use_bonus(self, req, hero):  # используем бонус, улучшаем героя
        hero["level"] += 1
