from .MonsterBase import MonsterBase


class Amazon(MonsterBase):
    def __init__(self):
        super(Amazon, self).__init__(
            8,
            'Амазонка',
            'Тебя вздула женщина! Ущемление гордости в тяжёлой форме. Потеряй расу.',
            2,
            1
        )

    def do_bad_things(self, req, hero):  # он не убежал
        hero["race"] = None
