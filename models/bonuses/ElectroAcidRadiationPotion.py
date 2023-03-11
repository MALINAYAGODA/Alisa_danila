from .BonusBase import BonusBase


class ElectroAcidRadiationPotion(BonusBase):
    def __init__(self):
        super(ElectroAcidRadiationPotion, self).__init__(
            'Электро-кислотно-радиационное зелье',
            'Играй в любой бой. +5 любой стороне. Разовая шмотка.',
            200,
            'Бонус +5'
        )

    def use_bonus(self, req, hero):  # используем бонус, улучшаем героя
        hero["bonus_strength"] += 5
    