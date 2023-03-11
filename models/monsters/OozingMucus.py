from .MonsterBase import MonsterBase


class OozingMucus(MonsterBase):
    def __init__(self):
        super(OozingMucus, self).__init__(
            1, 'Сочащаяся слизь',
            'Потеряй надетую обувку. Если нет обуви, потеряй уровень.',
            1, 1
        )

    def do_bad_things(self, req, hero):  # он не убежал
        if hero["armor"]["leg"] is None:
            hero["level"] = max(1, hero["level"] - 1)
        else:
            hero["armor"]["leg"] = None
