from .BonusBase import BonusBase


class MagicLamp(BonusBase):
    def __init__(self):
        super(MagicLamp, self).__init__(
            'Волшебная лампа',
            'Играй только в свой ход. Примчиться джин,прогонит одного монстра и ты сможешь взять '
            'сокровищя',
            500,
            'Монстры погибают'
        )

    def use_bonus(self, req, hero):  # используем бонус, улучшаем героя
        monster = hero["monster"]
        hero["monster"] = None
        return {'monster': monster}
