from .MonsterBase import MonsterBase


class GelatinOctahedron(MonsterBase):
    def __init__(self):
        super(GelatinOctahedron, self).__init__(2, 'Желатиновый октаэдр', 'Сбрось все свои шмотки.',
                                                1, 1)

    def do_bad_things(self, req, hero):  # он не убежал
        for i in hero["armor"].keys():
            hero["armor"][i] = None
