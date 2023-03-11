from .MonsterBase import MonsterBase


class TheKingIsHere(MonsterBase):
    def __init__(self):
        super(TheKingIsHere, self).__init__(
            16, 'Царь тут',
            'Сбрось все свои шмотки и всю руку!',
            4, 2
        )

    def do_bad_things(self, req, hero):  # он не убежал
        for i in hero["armor"].keys():
            hero["armor"][i] = None
        if len(hero["weapon"]) > 0:
            del hero["weapon"][0]
