from .BonusBase import BonusBase



class PeljeZutanica(BonusBase):
    def __init__(self):
        super(PeljeZutanica, self).__init__(
            'Пелье Зутаницы',
            'Играй в любой бой. +3 любой стороне. Разовая шмотка.',
            100,
            'Бонус +3'
        )

    def use_bonus(self, req, hero):  # используем бонус, улучшаем героя
        hero["bonus_strength"] += 3
    