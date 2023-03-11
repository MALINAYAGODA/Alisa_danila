from random import choice

from .CurseBase import CurseBase


class UnbearablyVileCurseLoseYourRandomStuff(CurseBase):
    def __init__(self):
        super(UnbearablyVileCurseLoseYourRandomStuff, self).__init__(
            'Невыносимо гнусное проклятие! Потеряй рандомную шмотку!'
        )

    def use_bad_things(self, req, hero):  # проклятье на нас
        lst = []
        for i in hero["armor"]:
            if hero["armor"][i] is not None:
                lst.append(i)
        if len(lst) != 0:
            hero["armor"][choice(lst)] = None
