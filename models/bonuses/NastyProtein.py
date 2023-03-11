from .BonusBase import BonusBase


class NastyProtein(BonusBase):
    def __init__(self):
        super(NastyProtein, self).__init__(
            'Противный Протеин',
            'Играй в любой бой. +2 любой стороне. Разовая шмотка.',
            200,
            'Бонус +2'
        )

    def use_bonus(self, req, hero):  # используем бонус, улучшаем героя
        hero["bonus_strength"] += 2
    