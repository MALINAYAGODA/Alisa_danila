from .BonusBase import BonusBase


class WallInstant(BonusBase):
    def __init__(self):
        super(WallInstant, self).__init__(
            'Стенка-мгновенка',
            'Все манчкины могут автоматически смыться из любого боя и получить сокровищя.',
            300,
            'Монстры погибают'
        )

    def use_bonus(self, req, hero):  # используем бонус, улучшаем героя
        monster = hero["monster"]
        hero["monster"] = None
        return {'monster': monster}
