from .RaceBase import RaceBase


class Halfling(RaceBase):
    def __init__(self):
        super().__init__(2, 'Хафлинги любят много покушать! Поэтому они получают +1 уровень за каждый пройденный путь!')
