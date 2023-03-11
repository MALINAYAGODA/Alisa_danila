import random
from .CurseBase import CurseBase


class YourWeaponWasStolenWhatSlobYouAre(CurseBase):
    def __init__(self):
        super(YourWeaponWasStolenWhatSlobYouAre, self).__init__(
            'У тебя украли оружие! Какой ты растяпа!'
        )

    def use_bad_things(self, req, hero):  # проклятье на нас
        if len(hero["weapon"]) != 0:
            del hero["weapon"][random.randint(0, len(hero["weapon"]))]
