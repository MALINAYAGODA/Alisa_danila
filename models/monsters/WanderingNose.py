from .MonsterBase import MonsterBase


class WanderingNose(MonsterBase):
    def __init__(self):
        super(WanderingNose, self).__init__(
            10, 'Блуждающий нос',
            'Он ещё тот нюхач, от него нельзя смыться. Ничто не поможет избежать напотребства. '
            'Потеряй 3 уровня.',
            3, 1
        )

    def do_bad_things(self, req, hero):  # он не убежал
        hero["level"] = max(1, hero["level"] - 3)
