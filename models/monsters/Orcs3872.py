import random

from .MonsterBase import MonsterBase


class Orcs3872(MonsterBase):
    def __init__(self):
        super(Orcs3872, self).__init__(
            10, '3872 орка',
            'Брось кубик. На 2 и меньше ты затопан до смерти, иначе потеряй столько уровней, '
            'сколько выпало.',
            3, 1
        )

    def do_bad_things(self, req, hero):  # он не убежал
        num = random.randint(1, 7)
        s = f"На кубике выпало {num}. "
        if num <= 2:
            hero["is_alive"] = False
            return {"responce": s}
        else:
            hero["level"] = max(1, hero["level"] - 2)
            return {"responce": s + f"Ваш уровень {hero['level']}."}
