from .BonusBase import BonusBase


class CoolBalls(BonusBase):
    def __init__(self):
        super(CoolBalls, self).__init__(
            'Клёвые шарики',
            'Играй в любой бой для отвлечения внимания. +5 любой стороне. Разовая шмотка.',
            500,
            'Бонус +3'
        )

    def use_bonus(self, req, hero):  # используем бонус, улучшаем героя
        hero["bonus_strength"] += 5
    