from .CurseBase import CurseBase


class LoseTheShoesYoureWearing(CurseBase):
    def __init__(self):
        super(LoseTheShoesYoureWearing, self).__init__(
            'Потеряй надетую обувку'
        )

    def use_bad_things(self, req, hero):  # проклятье на нас
        hero["armor"]["leg"] = None
