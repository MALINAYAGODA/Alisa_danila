from .BonusBase import BonusBase


class FlamePoisonPotion(BonusBase):
    def __init__(self):
        super(FlamePoisonPotion, self).__init__(
            'Зелье пламенной отравы',
            'Играй в любой бой. +3 любой стороне. Разовая шмотка.',
            100,
            'Бонус +3'
        )

    def use_bonus(self, req, hero):  # используем бонус, улучшаем героя
        hero["bonus_strength"] += 3
    