from .CurseBase import CurseBase


class Lose2LevelsSoThatItWontBeHabitToPickUpBirdsInTheDungeonsFromNowOn(CurseBase):
    def __init__(self):
        super(Lose2LevelsSoThatItWontBeHabitToPickUpBirdsInTheDungeonsFromNowOn, self).__init__(
            'Потеряй 2 уровня, чтобы не повадно было впредь подбирать птиц в подземельях'
        )

    def use_bad_things(self, req, hero):  # проклятье на нас
        hero["level"] = max(1, hero["level"] - 2)
