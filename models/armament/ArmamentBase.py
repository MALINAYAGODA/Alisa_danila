class ArmamentBase:  # вооружение
    def __init__(self, bonus, title, price, what, if_weapon_hand=0, *args, **kwargs):
        self.title = title
        self.bonus = bonus
        self.price = price
        self.what = what
        self.if_weapon_hand = if_weapon_hand

    def use_armament(self, req, hero):  # надеваем достпехи/оружие
        # в отдельную переменную доб бонус
        pass