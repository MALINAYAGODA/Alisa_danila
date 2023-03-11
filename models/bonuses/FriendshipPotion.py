from .BonusBase import BonusBase


class FriendshipPotion(BonusBase):
    def __init__(self):
        super(FriendshipPotion, self).__init__(
            'Зелье дружбы',
            'Играй в любой бой. Сбрось монстра и тут же тяни сокровища.',
            200,
            'Монстры погибают'
        )

    def use_bonus(self, req, hero):  # используем бонус, улучшаем героя
        hero["monster"] = None
    