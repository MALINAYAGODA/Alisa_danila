from .BonusBase import BonusBase


class PopumorphPotion(BonusBase):
    def __init__(self):
        super(PopumorphPotion, self).__init__(
            'Зелье попуморфа',
            'Играй в любой бой. Один монстр превращается в попугая и улетает, оставляя свои '
            'сокровища. Получи сокровищя без боя',
            1300,
            'Монстры погибают'
        )

    def use_bonus(self, req, hero):  # используем бонус, улучшаем героя
        monster = hero["monster"]
        hero["monster"] = None
        return {'monster': monster}
    