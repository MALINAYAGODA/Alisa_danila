from .BonusBase import BonusBase


class RocketOfMagicalPurpose(BonusBase):
    def __init__(self):
        super(RocketOfMagicalPurpose, self).__init__(
            'Ракета магического назначения',
            'Играй в любой бой. +5 любой стороне. Разовая шмотка.',
            300,
            'Бонус +5'
        )

    def use_bonus(self, req, hero):  # используем бонус, улучшаем героя
        hero["bonus_strength"] += 5
