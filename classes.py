class Monster:  # монстр
    def __init__(self, level, title, bad_things, count_gem, count_level):
        self.level = level
        self.title = title
        self.bad_things = bad_things
        self.count_gem = count_gem
        self.count_level = count_level

    def do_bad_things(self, req, hero):  # он не убежал
        hero['is_alive'] = False


class Bonus:  # бонус
    def __init__(self, title, additional_title, price, mini_text=None):
        self.title = title
        self.additional_title = additional_title
        self.price = price
        if mini_text is None:
            self.mini_text = 'без объяснения'
        else:
            self.mini_text = mini_text

    def use_bonus(self, req, hero):  # используем бонус, улучшаем героя
        hero["bonus_strength"] += 3


class Armament:  # вооружение
    def __init__(self, bonus, title, price, what, if_weapon_hand=None):
        self.title = title
        self.bonus = bonus
        self.price = price
        self.what = what
        if if_weapon_hand is None:
            self.if_weapon_hand = 0
        else:
            self.if_weapon_hand = if_weapon_hand


class Proklate:  # проклятье
    def __init__(self, title):
        self.title = title

    def use_bad_things(self, req, hero):  # проклятье на нас
        hero['level'] -= 0


class Race:  # раса
    def __init__(self, title, what):
        self.title = title
        self.what = what
