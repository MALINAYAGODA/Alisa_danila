from .CurseBase import CurseBase


class LoseTheFirebrandYoureWearing(CurseBase):
    def __init__(self):
        super(LoseTheFirebrandYoureWearing, self).__init__(
            'Потеряй надетый головняк.'
        )

    def use_bad_things(self, req, hero):  # проклятье на нас
        hero["armor"]["head"] = None
