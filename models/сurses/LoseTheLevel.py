from .CurseBase import CurseBase


class LoseTheLevel(CurseBase):
    def __init__(self):
        super(LoseTheLevel, self).__init__(
            'Потеряй уровень'
        )

    def use_bad_things(self, req, hero):  # проклятье на нас
        hero["level"] = max(1, hero["level"] - 1)

