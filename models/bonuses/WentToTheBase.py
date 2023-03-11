from .BonusBase import BonusBase


class WentToTheBase(BonusBase):
    def __init__(self):
        super(WentToTheBase, self).__init__(
            'Ушёл на базу',
            'Играй любой бой, чтобы отправить на отдых монстров из этой комнаты. Игрок, который '
            'должен был биться с ними, сбрасывает их карты и тут же тянет сокровища.',
            500,
            'Монстры погибают'
        )

    def use_bonus(self, req, hero):  # используем бонус, улучшаем героя
        monster = hero["monster"]
        hero["monster"] = None
        return {'monster': monster}
