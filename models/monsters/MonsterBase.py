class MonsterBase:  # монстр
    def __init__(self, level, title, bad_things, count_gem, count_level):
        self.level = level
        self.title = title
        self.bad_things = bad_things
        self.count_gem = count_gem
        self.count_level = count_level

    def fight_or_not(self, req, hero):  # убежать или драться? Сравнение силы
        pass # off

    def fight(self, req, hero):  # после использования бонусов, мы сражаемся и смотрим кто победил
        pass # off

    def do_bad_things(self, req, hero):  # он не убежал
        pass
