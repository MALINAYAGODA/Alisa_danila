from .MonsterBase import MonsterBase


class Gazebo(MonsterBase):
    def __init__(self):
        super(Gazebo, self).__init__(8, 'Газебо', 'Потеряй 3 уровня.', 2, 1)

    def do_bad_things(self, req, hero):  # он не убежал
        hero["level"] = max(1, hero["level"] - 3)
