from .MonsterBase import MonsterBase


class YoungBeauty(MonsterBase):
    def __init__(self):
        super(YoungBeauty, self).__init__(
            1, 'Молотая красотка',
            'Бьет баба молотом… Потеряй уровень.',
            1, 1
        )

    def do_bad_things(self, req, hero):  # он не убежал
        hero["level"] = max(1, hero["level"] - 1)
