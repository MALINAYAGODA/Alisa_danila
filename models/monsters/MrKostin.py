from .MonsterBase import MonsterBase


class MrKostin(MonsterBase):
    def __init__(self):
        super(MrKostin, self).__init__(
            2, 'Г-н Костин',
            'Его костлявые прикосновения снимают с тебя 2 уровня.',
            1, 1
        )

    def do_bad_things(self, req, hero):  # он не убежал
        hero["level"] = max(1, hero["level"] - 2)
